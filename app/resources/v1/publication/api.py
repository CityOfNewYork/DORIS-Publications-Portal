from flask import request
from flask_restful import Resource
from app.resources.lib import api_response
from app.models import Publication
from .forms import SubmitForm
from flask_login import login_required


class PublicationAPI(Resource):

    def get(self, id):
        pub = Publication(id,
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
            pub = Publication(1,  # id
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