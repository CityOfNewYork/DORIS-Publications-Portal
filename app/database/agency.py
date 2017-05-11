import csv
from . import db, _utils
from app.models import Agency
from flask import current_app


def get(ein):
    """
    Returns an agency object with the supplied identifier or
    returns None if the agency cannot be found.
    :rtype: models.Agency
    """
    return _utils.get(Agency, ein)


def create(ein, name, acronym=None, parent_ein=None):
    """
    Creates an agency database record and returns the created agency object.
    :rtype: models.Agency
    """
    return _utils.create(
        Agency,
        name,
        acronym,
        parent_ein
    )


def update(ein, name=None, acronym=None, parent_ein=None):
    """
    Updates an agency database record.
    """
    _utils.update(
        Agency,
        {"ein": ein},
        name=name,
        acronym=acronym,
        parent_ein=parent_ein
    )


def delete(ein):
    """
    Deletes an agency database record.
    """
    _utils.delete(Agency, ein)


def populate_from_csv(csv_name=None):
    """
    Populate agency table with data from csv file.
    """
    filename = csv_name or current_app.config['AGENCY_DATA_CSV']
    with open(filename, 'r') as data:
        dict_reader = csv.DictReader(data)
        for row in dict_reader:
            if get(row['ein']) is None:  # if no dupes
                agency = Agency(
                    row['ein'],
                    row['name'],
                    row['acronym'] or None,
                    row['parent_ein'] or None,
                )
                db.session.add(agency)
        db.session.commit()
