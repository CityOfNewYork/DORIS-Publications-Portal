from flask import request
from flask_restful import Resource
from app.resources.lib import api_response
# from app.models import Document
from .forms import SubmitForm
from flask_login import login_required


from collections import namedtuple
Document = namedtuple("Document", ["id", "title", "type", "description"])


class PublicationAPI(Resource):

    def get(self, id):
        pub = Document(id,
                       'A Title',
                       'TYPE',
                       'A description.')
        return api_response.success({
            'publication': {
                'id': pub.id,
                'title': pub.title,
                'type': pub.type,
                'description': pub.description,
            }
        })

    @login_required
    def post(self):
        try:
            form = SubmitForm(data=request.get_json(force=True))
        except Exception as e:
            return api_response.error(str(e))

        if form.validate():
            # create publication
            pub = Document(1,  # id
                           form.title.data,
                           form.type.data,
                           form.description.data)  # TODO: combined files name
            return api_response.success({
                'publication': {
                    'id': pub.id,
                    'title': pub.title,
                    'type': pub.type,
                    'description': pub.description,
                }
            })
        return api_response.fail(form.errors)


class PublicationsApi(Resource):  # FIXME: this will probably never be used due to SearchApi

    def get(self):
        # return multiple publications
        pass
