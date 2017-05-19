from flask import request
from flask_restful import Resource
from app.resources.lib import api_response
# from app.models import Document
from .forms import SubmitForm
from flask_login import login_required

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
            form = SubmitForm('some_ID', data=request.get_json(force=True))
        except Exception as e:
            return api_response.error(str(e))

        if form.validate():
            # create document
            doc = Document(1,  # id
                           form.title.data,
                           form.type.data,
                           form.description.data)  # TODO: combined files name
            return api_response.success({
                'publication': {
                    'id': doc.id,
                    'title': doc.title,
                    'type': doc.type,
                    'description': doc.description,
                }
            })
        return api_response.fail(form.errors)
