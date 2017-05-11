from . import _utils
from app.models import DocumentEvent


def get(id):
    """
    Returns a document event object with the supplied identifier or
    returns None if the agency cannot be found. 
    :rtype: models.DocumentEvent
    """
    return _utils.get(DocumentEvent, id)


def create(user_guid, user_auth_type, document_id, action, state=None):
    """
    Creates a document event record and returns the created event object.
    :rtype: models.DocumentEvent
    """
    return _utils.create(
        DocumentEvent,
        user_guid,
        user_auth_type,
        document_id,
        action,
        state
    )
