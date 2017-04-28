from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .agency import Agency
from .registration import Registration
