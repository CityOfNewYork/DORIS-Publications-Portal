import os
from os import environ as env
from collections import namedtuple
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

DEV = 'development'
TST = 'testing'
PRD = 'production'


class Config(object):
    SECRET_KEY = env.get('SECRET_KEY') or 'you better change me or else'

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://gpp_db@127.0.0.1:5432/gpp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # disables warning

    # Data
    AGENCY_DATA_CSV = env.get('AGENCY_DATA_CSV') or os.path.join(basedir, 'data', 'agencies.csv')
    REPORT_TYPE_CSV = env.get('REPORT_TYPE_CSV') or os.path.join(basedir, 'data', 'report_type.csv')

    UPLOAD_DIRECTORY = env.get('UPLOAD_DIRECORY') or os.path.join(basedir, 'uploads')

    SCHEMAS_DIRECTORY = env.get('SCHEMAS_DIRECTORY') or os.path.join(basedir, 'app/schemas')

    # Redis Settings
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = os.environ.get('REDIS_PORT') or '6379'
    CELERY_REDIS_DB = 0
    SESSION_REDIS_DB = 1
    EMAIL_REDIS_DB = 2

    # Celery Settings
    CELERY_BROKER_URL = 'redis://{redis_host}:{redis_port}/{celery_redis_db}'.format(
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        celery_redis_db=CELERY_REDIS_DB
    )
    CELERY_RESULT_BACKEND = 'redis://{redis_host}:{redis_port}/{celery_redis_db}'.format(
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        celery_redis_db=CELERY_REDIS_DB
    )

    # Flask-Mail Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 2500
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX') or '[Submissions Portal]'
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'Submissions Portal <donotreply@records.nyc.gov>'


class ConfigDevelopment(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class ConfigTesting(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False  # TODO: should this be True?

    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_TEST_DATABASE_URI') or 'postgresql://gpp_db@127.0.0.1:5432/gpp_test'


class ConfigProduction(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = True


config = {
    DEV: ConfigDevelopment,
    TST: ConfigTesting,
    PRD: ConfigProduction,
}
