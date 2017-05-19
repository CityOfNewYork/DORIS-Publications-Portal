import os
import magic
from flask import request, current_app
from flask_restful import Resource
from werkzeug.utils import secure_filename
from app.resources.lib import api_response
from flask_login import login_required


class UploadAPI(Resource):

    @login_required
    def post(self, dirname):
        """
        Save an uploaded file or reject it if it is not a PDF.
        
        :param dirname: name of directory within the uploads directory in which to save the uploaded file
        """
        files = request.files
        file_ = files[next(files.keys())]
        if self._file_is_pdf(file_):
            upload_path = os.path.join(
                current_app.config["UPLOAD_DIRECTORY"],
                dirname
            )
            # upload_path = /uploads/123
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            filename = secure_filename(file_.filename)
            upload_path = os.path.join(upload_path, filename)
            # upload_path = /uploads/123/file.pdf
            file_.save(upload_path)
            response_data = {
                "name": filename,
                "size": os.path.getsize(upload_path)
            }
            return api_response.success(response_data)
        else:
            return api_response.fail("This is not a PDF file. Please remove.")

    @login_required
    def delete(self, dirname, filename):
        """
        Delete a previously uploaded file.
        
        :param dirname: name of directory within the uploads directory where file is stored
        :param filename: name of previously uploaded file
        """
        filename = secure_filename(filename)

        upload_path = os.path.join(
            current_app.config["UPLOAD_DIRECTORY"],
            dirname,
            filename
        )
        if os.path.exists(upload_path):
            os.remove(upload_path)
            return api_response.success({
                "name": filename
            })
        return api_response.fail(
            "File '{}' not found.".format(filename)
        )

    def _file_is_pdf(self, file_):
        is_pdf = magic.from_buffer(file_.read(1024), mime=True) == "application/pdf"
        file_.seek(0)
        return is_pdf
