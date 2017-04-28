import csv
from . import db
from .utils import Object, session_context
from app import models
from flask import current_app


class Agency(Object):

    @classmethod
    def get(cls, ein):
        """
        Returns an agency object with the supplied identifier or
        returns None if the agency cannot be found.
        :rtype: models.Agency
        """
        return models.Agency.query.get(ein)

    @staticmethod
    def create(ein, name, acronym=None, parent_ein=None):
        """
        Creates an agency database record and returns the created agency object.
        :rtype: models.Agency
        """
        agency = models.Agency(
            ein,
            name,
            acronym,
            parent_ein,
        )
        with session_context():
            db.session.add(agency)
        return agency

    @staticmethod
    def update(ein, name=None, acronym=None, parent_ein=None):
        """
        Updates an agency database record.
        """
        if (name or acronym or parent_ein):
            with session_context():
                models.Agency.query.filter_by(
                    ein=ein
                ).update({
                    col: val for col, val in {
                        models.Agency.name: name,
                        models.Agency.acronym: acronym,
                        models.Agency.parent_ein: parent_ein
                    }.items() if val is not None
                })

    @classmethod
    def delete(cls, ein):
        super().delete(ein)

    @classmethod
    def populate_from_csv(cls, csv_name=None):
        """
        Populate agency table with data from csv file.
        """
        filename = csv_name or current_app.config['AGENCY_DATA_CSV']
        with open(filename, 'r') as data:
            dictreader = csv.DictReader(data)
            for row in dictreader:
                if cls.get(row['ein']) is None:  # if no dupes
                    agency = models.Agency(
                        row['ein'],
                        row['name'],
                        row['acronym'] or None,
                        row['parent_ein'] or None,
                    )
                    db.session.add(agency)
            db.session.commit()
