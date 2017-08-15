import redis
from flask import Flask
from flask_login import LoginManager
from flask_kvsession import KVSessionExtension
from flask_wtf.csrf import CSRFProtect
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore
from config import config
from app.database import db
from app.models import User
from app.constants import USER_ID_DELIMETER
from app.resources.lib import api_response

store = RedisStore(redis.StrictRedis(db=0, host='localhost', port='6379'))
prefixed_store = PrefixDecorator("session_", store)

csrf = CSRFProtect()
login_manager = LoginManager()
session = KVSessionExtension()


@login_manager.user_loader
def load_user(user_id):
    user_id = user_id.split(USER_ID_DELIMETER)
    return User.query.filter_by(
        guid=user_id[0],
        auth_type=user_id[1]
    ).first()


@login_manager.unauthorized_handler
def unauthorized():
    return api_response.fail("You do not have the authorization to do this.", 403)


def create_app(conf_type):
    app = Flask(__name__)
    app.config.from_object(config[conf_type])

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    session.init_app(app, prefixed_store)

    from .resources import v1
    from .main.views import main
    from flask import Blueprint
    from flask_restful import Api

    # initialize blueprint
    blueprint = Blueprint('1.0', __name__)
    api = Api(blueprint)

    # Add resource routes
    api.add_resource(v1.Documents, '/documents', '/documents/<int:id>')
    api.add_resource(v1.Upload, '/upload/<string:dirname>', '/upload/<string:dirname>/<string:filename>')
    api.add_resource(v1.Subjects, '/subjects')
    api.add_resource(v1.ReportTypes, '/report_types')
    api.add_resource(v1.Auth, '/auth')
    api.add_resource(v1.Languages, '/languages')

    # Register blueprints
    app.register_blueprint(blueprint, url_prefix="/api/v1.0")
    app.register_blueprint(main)

    return app
