from . import db
from ._utils import Object, session_context
from app import models


class Registration(Object):

    @staticmethod
    def get(id):
        """
        Returns an agency object with the supplied identifier or
        returns None if the agency cannot be found.
        :rtype: models.Registration
        """
        return super(Registration, Registration)._get(models.Registration, id)

    @staticmethod
    def create(user_guid, user_auth_type, agency_ein):
        """
        Creates an agency database record and returns the created agency object.
        :rtype: models.Registration
        """
        return super(Registration, Registration)._create(
            models.Registration,
            user_guid,
            user_auth_type,
            agency_ein
        )
