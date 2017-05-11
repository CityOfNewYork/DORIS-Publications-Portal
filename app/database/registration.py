from . import _utils, registration_event, user
from app.models import Registration
from app.constants import registration_action


def get(id):
    """
    Returns an agency object with the supplied identifier or
    returns None if the agency cannot be found.
    :rtype: Registration
    """
    return _utils.get(Registration, id)


def create(user_guid, user_auth_type, agency_ein):
    """
    Creates an agency database record and returns the created agency object.
    :rtype: Registration
    """
    return _utils.create(
        Registration,
        user_guid,
        user_auth_type,
        agency_ein
    )


def create_and_submit(registrant_guid,
                      registrant_auth_type,
                      agency_ein):
    """
    Creates a registration record and its associated submission event record.
    The registrant is the agent (user performing an action) for the submission event.
    :rtype: Registration
    """
    registration = create(registrant_guid, registrant_auth_type, agency_ein)
    registration_event.create(registrant_guid, registrant_auth_type, registration.id, registration_action.SUBMITTED)
    return registration


def deny(id, agent_guid, agent_auth_type):
    """
    Creates a registration denial event record if a registration has already been submitted.
    The user approving the registration cannot be the registrant.
    """
    _resolve(id, agent_guid, agent_auth_type, registration_action.DENIED)


def approve(id, agent_guid, agent_auth_type):
    """
    Creates a registration approval event record if a registration has already been submitted.
    The user denying the registration cannot be the registrant.
    """
    _resolve(id, agent_guid, agent_auth_type, registration_action.APPROVED)


def _resolve(id, agent_guid, agent_auth_type, action):
    registration = get(id)
    agent = user.get(agent_guid, agent_auth_type)
    if registration.is_pending and registration.registrant != agent:
        registration_event.create(agent_guid, agent_auth_type, id, action)