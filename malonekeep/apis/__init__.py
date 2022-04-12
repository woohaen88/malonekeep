from flask import (Blueprint,
                   g,
                   abort)
from flask_restx import Api
from malonekeep.apis.user import ns as UserNameSpace
from malonekeep.apis.memo import ns as MemoNameSpace
from functools import wraps

def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401)
        return func(*args, **kwargs)
    return __wrapper


blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    blueprint,
    title="Malone Keep API",
    version="1.0",
    doc="/docs",
    decorators=[check_session],
    description="welcome my api docs"
)

api.add_namespace(UserNameSpace)
api.add_namespace(MemoNameSpace)