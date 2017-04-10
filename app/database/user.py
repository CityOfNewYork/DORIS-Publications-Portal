from . import db
from .utils import Object, session_context
from app import models


class User(Object):

    @staticmethod
    def get(guid, auth_type):
        """ 
        Returns a user object with the supplied identifiers or 
        returns None if the user cannot be found. 
        """
        return models.User.query.get((guid, auth_type))

    @staticmethod
    def get_by_email(email):
        """
        Returns a user object with the supplied email or 
        returns None if the user cannot be found.
        """
        return models.User.query.filter_by(email=email).one_or_none()

    @staticmethod
    def create(guid, auth_type, first_name, middle_initial, last_name, email):
        """ 
        Creates a user database record and returns the created user object.
        """
        user = models.User(
            guid,
            auth_type,
            first_name,
            middle_initial,
            last_name,
            email,
            email_validated=False,
            terms_of_use_accepted=False
        )
        with session_context():
            db.session.add(user)
        return user

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass
