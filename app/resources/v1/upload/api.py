import os
from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from app.resources.lib import api_response
from flask_login import login_required


class UploadAPI(Resource):

    @login_required
    def post(self):
        files = request.files
        file_ = files[next(files.keys())]
        filename = secure_filename(file_.filename)
        upload_path = os.path.join(
            current_app.config["UPLOAD_DIRECTORY"],
            filename
        )
        file_.save(upload_path)
        response_data = {
            "name": filename,
            "size": os.path.getsize(upload_path)
        }
        return api_response.success(response_data)

    @login_required
    def delete(self, filename):
        filename = secure_filename(filename)

        upload_path = os.path.join(
            current_app.config["UPLOAD_DIRECTORY"],
            filename
        )
        if os.path.exists(upload_path):
            os.remove(upload_path)
            return api_response.success({
                "name": filename
            })
        return api_response.fail(
            'File "{}" not found.'.format(filename)
        )
