from . import db
from .utils import Object, session_context
from app import models


class Registration(Object):

    @classmethod
    def get(cls, id):
        """
        Returns an agency object with the supplied identifier or
        returns None if the agency cannot be found.
        :rtype: models.Registration
        """
        return models.Registration.query.get(id)

    @staticmethod
    def create(registrant_guid, registrant_auth_type, agency_ein):
        """
        Creates an agency database record and returns the created agency object.
        :rtype: models.Registration
        """
        registration = models.Registration(
            registrant_guid,
            registrant_auth_type,
            agency_ein
        )
        with session_context():
            db.session.add(registration)
        return registration

    @classmethod
    def delete(cls, id):
        super().delete(id)
