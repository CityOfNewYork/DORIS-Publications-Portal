from . import _utils
from app.models import User


def get(guid, auth_type):
    """ 
    Returns a user object with the supplied identifiers or 
    returns None if the user cannot be found.
    :rtype: models.User
    """
    return _utils.get(User, (guid, auth_type))


def get_first():
    """
    Returns a single user object or None if there are no users present.
    :rtype: models.User
    """
    return User.query.first()


def get_by_email(email):
    """
    Returns a user object with the supplied email or 
    returns None if the user cannot be found.
    :rtype: models.User
    """
    return User.query.filter_by(email=email).one_or_none()


def create(guid, auth_type, first_name, middle_initial, last_name, email):
    """ 
    Creates a user database record and returns the created user object.
    :rtype: models.User
    """
    return _utils.create(
        User,
        guid,
        auth_type,
        first_name,
        middle_initial,
        last_name,
        email,
        email_validated=False,
        terms_of_use_accepted=False
    )


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
    _utils.update(
        User,
        {"guid": guid, "auth_type": auth_type},
        phone=phone,
        email_validated=email_validated,
        terms_of_use_accepted=terms_of_use_accepted,
        is_poc=is_poc,
        is_library=is_library,
        is_super=is_super
    )


def delete(guid, auth_type):
    """
    Deletes a user database record.
    """
    _utils.delete(User, (guid, auth_type))
