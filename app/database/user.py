from . import db
from .utils import Object, session_context
from app import models


class User(Object):

    @classmethod
    def get(cls, guid, auth_type):
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
    def update(guid,
               auth_type,
               phone=None,
               email_validated=None,
               terms_of_use_accepted=None,
               is_poc=None,
               is_library=None,
               is_super=None):
        """
        Updates a user database record. 
        """
        if (
            phone or
            email_validated or
            terms_of_use_accepted or
            is_poc or
            is_library or
            is_super
        ):
            with session_context():
                models.User.query.filter_by(
                    guid=guid,
                    auth_type=auth_type
                ).update({
                    col: val for col, val in {
                        models.User.phone: phone,
                        models.User.email_validated: email_validated,
                        models.User.terms_of_use_accepted: terms_of_use_accepted,
                        models.User.is_poc: is_poc,
                        models.User.is_library: is_library,
                        models.User.is_super: is_super
                    }.items() if val is not None
                })

    @classmethod
    def delete(cls, guid, auth_type):
        """
        Deletes a user database record.
        """
        user = cls.get(guid, auth_type)
        with session_context:
            db.session.delete(user)
