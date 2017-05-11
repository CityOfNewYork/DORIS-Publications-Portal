from . import _utils
from app.models import RegistrationEvent


def get(id):
    """
    Returns a registration event object with the supplied identifier or
    returns None if the agency cannot be found. 
    :rtype: models.RegistrationEvent
    """
    return _utils.get(RegistrationEvent, id)


def create(user_guid, user_auth_type, registration_id, action):
    """
    Creates a registration event record and returns the created event object.

    An event cannot be created when another event with the same action exists for the supplied registration id
    (this is handled with a UNIQUE constraint).
    
    :rtype: models.RegistrationEvent
    """
    return _utils.create(
        RegistrationEvent,
        user_guid,
        user_auth_type,
        registration_id,
        action,
    )
