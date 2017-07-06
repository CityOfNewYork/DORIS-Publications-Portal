import csv
from flask import current_app
from . import db
from app.models import ReportType


def get_from_value(value):
    """
    Retuns a report_type object with the supplied identifier or
    returns None if the report_type cannot be found.
    :rtype: models.ReportType
    """
    return ReportType.query.filter_by(value=value).one_or_none()


def populate_from_csv(csv_name=None):
    """
    Populate report_type table with data from csv file.
    """
    filename = csv_name or current_app.config['REPORT_TYPE_CSV']
    with open(filename, 'r') as data:
        dict_reader = csv.DictReader(data)
        for row in dict_reader:
            if get_from_value(row['value']) is None:
                report_type = ReportType(
                    row['name'],
                    row['value']
                )
                db.session.add(report_type)
        db.session.commit()
