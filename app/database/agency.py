import csv
from . import db
from ._utils import Object, session_context
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
        return super(Agency, Agency)._get(models.Agency, ein)

    @staticmethod
    def create(ein, name, acronym=None, parent_ein=None):
        """
        Creates an agency database record and returns the created agency object.
        :rtype: models.Agency
        """
        return super(Agency, Agency)._create(
            models.Agency,
            name,
            acronym,
            parent_ein
        )

    @staticmethod
    def update(ein, name=None, acronym=None, parent_ein=None):
        """
        Updates an agency database record.
        """
        super(Agency, Agency)._update(
            models.Agency,
            {"ein": ein},
            name=name,
            acronym=acronym,
            parent_ein=parent_ein
        )

    @staticmethod
    def delete(ein):
        """
        Deletes an agency database record.
        """
        super(Agency, Agency)._delete(models.Agency, ein)

    @classmethod
    def populate_from_csv(cls, csv_name=None):
        """
        Populate agency table with data from csv file.
        """
        filename = csv_name or current_app.config['AGENCY_DATA_CSV']
        with open(filename, 'r') as data:
            dict_reader = csv.DictReader(data)
            for row in dict_reader:
                if cls.get(row['ein']) is None:  # if no dupes
                    agency = models.Agency(
                        row['ein'],
                        row['name'],
                        row['acronym'] or None,
                        row['parent_ein'] or None,
                    )
                    db.session.add(agency)
            db.session.commit()
