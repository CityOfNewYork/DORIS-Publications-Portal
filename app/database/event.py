from . import db
from ._utils import Object, session_context
from .registration import Registration
from app import models


class DocumentEvent(Object):

    @staticmethod
    def get(id):
        """
        Returns a registration event object with the supplied identifier or
        returns None if the agency cannot be found. 
        :rtype: models.DocumentEvent
        """
        return super(DocumentEvent, DocumentEvent)._get(models.DocumentEvent, id)

    @staticmethod
    def create(user_guid, user_auth_type, registration_id, action, state=None):
        """
        Creates a registration event record and returns the created event object.
        :rtype: models.DocumentEvent
        """
        return super(DocumentEvent, DocumentEvent)._create(
            models.DocumentEvent,
            user_guid,
            user_auth_type,
            registration_id,
            action,
            state
        )


class RegistrationEvent(Object):

    @staticmethod
    def get(id):
        """
        Returns a registration event object with the supplied identifier or
        returns None if the agency cannot be found. 
        :rtype: models.RegistrationEvent
        """
        return super(RegistrationEvent, RegistrationEvent)._get(models.RegistrationEvent, id)

    @staticmethod
    def create(user_guid, user_auth_type, registration_id, action):
        """
        Creates a registration event record and returns the created event object.
        
        A submission event cannot be created 
            
            An event cannot be created when another event with the same action exists (handled by UNIQUE constraint)
            
        :rtype: models.RegistrationEvent
        """

        return super(RegistrationEvent, RegistrationEvent)._create(
            models.RegistrationEvent,
            user_guid,
            user_auth_type,
            registration_id,
            action,
        )
