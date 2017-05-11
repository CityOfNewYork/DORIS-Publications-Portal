from . import db
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


def create(model, *args, **kwargs):
    """
    Creates and returns a database object.
    """
    obj = model(*args, **kwargs)
    with session_context():
        db.session.add(obj)
    return obj


def get(model, key):
    """
    Retrieves and returns a database object for the specified model with the supplied identifier.
    """
    return model.query.get(key)


def update(model, key, **kwargs):
    """ 
    Updates a database object.
    The keyword arguments provided MUST correspond to column names for fields that will be updated.
    
    :type key: dict
    """
    if any(kwargs):
        with session_context():
            model.query.filter_by(
                **key
            ).update(
                {col: val for col, val in kwargs.items() if val is not None}
            )


def delete(model, key):
    """
    Deletes a database record.
    """
    obj = get(model, key)
    if obj is not None:
        with session_context:
            db.session.delete(obj)
