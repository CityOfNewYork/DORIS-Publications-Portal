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
    SECRET_KEY = env.get('SECRET_KEY') or 'you better change me'

    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # disables warning

    UPLOAD_DIRECTORY = env.get('UPLOAD_DIRECORY') or os.path.join(basedir, 'uploads')


class ConfigDevelopment(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class ConfigTesting(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True


class ConfigProduction(Config):
    DEBUG = False
    WTF_CSRF_ENABLED = True


config = {
    DEV: ConfigDevelopment,
    TST: ConfigTesting,
    PRD: ConfigProduction,
}
