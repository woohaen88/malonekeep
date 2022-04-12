class Config(object):

    '''FLASK CONFIG'''
    SECRET_KEY = 'secret'
    SESSION_COOKIE_NAME = 'malonekeep'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/malonekeep?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'

class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG=True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    TEMPLATES_AUTO_RELOAD = True
    # TODO: Front호출시 토큰 삽입
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Flask Config for Production"""
    pass