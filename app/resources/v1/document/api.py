from flask import request
from flask_restful import Resource
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
        "subtitle",
        "agency",
        "creators",
        "type",
        "subjects",
        "date_published",
        "year",
        "start_date",
        "end_date",
        "description"
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
        if not errors:
            # create document
            doc = Document(1,  # id
                           json.title)
            return api_response.success({
                'publication': {
                    'id': doc.id,
                    'title': doc.title,
                }
            })
        return api_response.fail(errors)
