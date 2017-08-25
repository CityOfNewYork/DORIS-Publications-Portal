from . import _utils
from app.models import Document


def get(id):
    """
    Returns a document object with the supplied identifier or
    returns None if the document cannot be found.
    :rtype: models.Document
    """
    return _utils.get(Document, id)


def create(user_guid,
           user_auth_type,
           title,
           creators,
           report_type,
           subjects,
           language,
           date_published,
           report_year_type,
           report_year_start,
           report_year_end,
           status,
           description,
           subtitle=None):
    """
    Creates a document database record and returns the created document object.
    :rtype: models.Document
    """
    return _utils.create(
        Document,
        user_guid,
        user_auth_type,
        title,
        creators,
        report_type,
        subjects,
        language,
        date_published,
        report_year_type,
        report_year_start,
        report_year_end,
        description,
        status,
        subtitle
    )
