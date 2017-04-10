from . import db
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError


@contextmanager
def session_context():
    """
    Provide a transactional scope around a series of operations.
    No session is created or closed since Flask-SQLAlchemy provides a session scope.
    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it 
    """
    try:
        yield
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise SQLAlchemyError(e)


class Object(metaclass=ABCMeta):
    """ Abstract base class for database objects. """

    @staticmethod
    @abstractmethod
    def get():
        """ Retrieves and returns a database object with the supplied identifier. """
        return

    @staticmethod
    @abstractmethod
    def create():
        """ Creates and returns a database object. """
        return

    @staticmethod
    @abstractmethod
    def update():
        """ Updates and returns a database object. """
        return

    @staticmethod
    @abstractmethod
    def delete():
        """ Deletes a database record. """
        return
