from flask import request
from flask_restful import Resource
from datetime import datetime
from app.resources.lib import api_response
# from app.models import Document
from app.resources.lib.schema_utils import validate_json
from flask_login import login_required

SCHEMA_PATH = 'v1/document/'

# TODO: use db object
from collections import namedtuple

Document = namedtuple(
    "Document", [
        "id",
        "title",
        # "subtitle",
        # "agency",
        # "creators",
        # "type",
        # "subjects",
        # "date_published",
        # "year",
        # "start_date",
        # "end_date",
        # "description"
    ]
)


class DocumentAPI(Resource):
    def get(self, id):
        doc = Document(id,
                       'A Title',
                       'TYPE',
                       'A description.')
        return api_response.success({
            'document': {
                'id': doc.id,
                'title': doc.title,
                'type': doc.type,
                'description': doc.description,
            }
        })

    @login_required
    def post(self):
        try:
            json = request.get_json(force=True)
        except Exception as e:
            return api_response.error(str(e))

        errors = validate_json(json, SCHEMA_PATH, 'submission')

        # validate publication date
        if errors.get("date_published") is None:
            # TODO: offset by timezone
            if datetime.strptime(json.get("date_published"), "%m/%d/%Y") > datetime.now():
                errors["date_published"] = ["This value exceeds the maximum allowable date."]

        # validate start and end dates
        if errors.get("start_date") is None and errors.get("end_date") is None:
            start = json.get("start_date")
            end = json.get("end_date")
            if start is not None and end is not None:
                # TODO: offset by timezone
                start = datetime.strptime(start, "%m/%d/%Y")
                end = datetime.strptime(end, "%m/%d/%Y")
                if start >= end:
                    errors["start_date"] = ["This date must be less than the end date."]
                    errors["end_date"] = ["This date must be greater than the start date."]

        if not errors:
            # create document
            doc = Document(1,  # id
                           json['title'])
            return api_response.success({
                'publication': {
                    'id': doc.id,
                    'title': doc.title,
                }
            })
        return api_response.fail(errors)
