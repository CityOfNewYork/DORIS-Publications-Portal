from flask_restful import Resource
from app.resources.lib import api_response
from app.constants.language import ALL


class LanguagesAPI(Resource):
    def get(self):
        """
        Get a list of the languages' text and value.

        :return: JSON response
        """
        return api_response.success([
            {
                "text": language.text,
                "value": language.value
            } for language in ALL
        ])
