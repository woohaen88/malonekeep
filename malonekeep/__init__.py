from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config=None):
    app = Flask(__name__)

    ''' Flask configuration '''
    from malonekeep.configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config['DEBUG']:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()

    print('run with:', config)
    app.config.from_object(config)

    

    ''' CSRF Init '''
    csrf.init_app(app)

    '''API'''
    from malonekeep.apis import blueprint as api
    app.register_blueprint(api)


    '''ROUTE INIT'''
    from malonekeep.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    '''DB INIT'''
    db.init_app(app)
    migrate.init_app(app, db)

    '''FLASK HOOK'''
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.before_request
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    return app