import os
from flask import (
    request,
    current_app
)
from flask_restful import Resource
from werkzeug.utils import secure_filename
from datetime import datetime
from app.resources.lib import api_response
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
        "report_type",
        "subjects",
        "language",
        "date_published",
        "year",
        "start_date",
        "end_date",
        "description"
    ]
)


class DocumentsAPI(Resource):
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
        """
        Handle the submission of a document.

        Example Request Payload:
            {
                "title": "testing123",
                "agency": "doris",
                "report_type": "adjudications_decisions",
                "subjects":[
                    "advertising"
                ],
                "description": "testing description",
                "files":[
                    {
                        "title":"test",
                        "name":"DT-38764594-150317-1628.pdf"
                    }
                ],
                "date_published":"06/20/2017",
                "year_type":"calendar",
                "year":1600
            }

        :return: JSON response
        """
        try:
            json = request.get_json(force=True)
            # TODO: utility for stripping values
        except Exception as e:
            return api_response.error(str(e))

        errors = validate_json(json, SCHEMA_PATH, 'submission')

        # validate files
        if errors.get("files") is None:
            file_errors = []
            for file_ in json["files"]:
                if not os.path.exists(
                        os.path.join(
                            current_app.config["UPLOAD_DIRECTORY"],
                            "some_ID",
                            secure_filename(file_["name"])
                        )
                ):
                    file_errors.append(
                        "{} : There was an error submitting this file. Please remove and re-upload.".format(
                            file_["name"]))
            if file_errors:
                errors["files"] = file_errors
        else:
            errors["files"] = [
                "There was an issue submitting your file(s). "
                "Please make sure you have entered a title for every file."
            ]

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
                    errors["start_date"] = ["This date must be earlier than the end date."]
                    errors["end_date"] = ["This date must be later than the start date."]

        if not errors:
            # create document
            doc = Document(1,  # id
                           json["title"],
                           json.get("subtitle"),
                           json["agency"],
                           json.get("creators"),
                           json["report_type"],
                           json["subjects"],
                           json["language"],
                           json["date_published"],
                           json.get("year"),
                           json.get("start_date"),
                           json.get("end_date"),
                           json["description"])
            return api_response.success({
                "document": {
                    "id": doc.id,
                    "title": doc.title,
                    "subtitle": doc.subtitle,
                    "agency": doc.agency,
                    "creators": doc.creators,
                    "report_type": doc.report_type,
                    "subjects": doc.subjects,
                    "language": doc.language,
                    "date_published": doc.date_published,
                    "year": doc.year,
                    "start_date": doc.start_date,
                    "end_date": doc.end_date,
                    "description": doc.description
                },
                "success_message": {
                    "text": "Your publication has been submitted for approval."
                }
            })
        return api_response.fail(errors)

    @login_required
    def patch(self, doc_id):
        # TODO: edits once document is created
        pass
