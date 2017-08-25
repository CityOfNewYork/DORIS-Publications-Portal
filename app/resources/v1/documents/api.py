import os
from flask import (
    request,
    current_app
)
from flask_login import login_required, current_user
from flask_restful import Resource
from werkzeug.utils import secure_filename
from datetime import datetime
from app.constants.document_action import SUBMITTED
from app.constants import report_year_type
from app.database.document import create
from app.resources.lib import api_response
from app.resources.lib.email_utils import send_email
from app.resources.lib.schema_utils import validate_json

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
        start = None
        end = None
        if json['year_type'] == report_year_type.OTHER and errors.get("start_date") is None and errors.get(
                "end_date") is None:
            start = json.get("start_date")
            end = json.get("end_date")
            if start is not None and end is not None:
                # TODO: offset by timezone
                start = datetime.strptime(start, "%m/%d/%Y")
                end = datetime.strptime(end, "%m/%d/%Y")
                if start >= end:
                    errors["start_date"] = ["This date must be earlier than the end date."]
                    errors["end_date"] = ["This date must be later than the start date."]

        if json['year_type'] in (report_year_type.CALENDAR, report_year_type.FISCAL):
            year = json['year']
            start_string = '{}/{}/{}'.format('01', '01', year)
            end_string = '{}/{}/{}'.format('12', '12', year)
            start = datetime.strptime(start_string, '%m/%d/%Y')
            end = datetime.strptime(end_string, '%m/%d/%Y')

        # create creators
        creators = {
            "primary_agency": json['agency'],
            "additional_creators": json.get('creators')
        }

        if not errors:
            # create document
            doc = create(current_user.guid,
                         current_user.auth_type,
                         json['title'],
                         creators,
                         json['report_type'],
                         json['subjects'],
                         json['language'],
                         json['date_published'],
                         json['year_type'],
                         start,
                         end,
                         SUBMITTED,
                         json['description'],
                         json.get('subtitle')
                         )
            send_email('Document Submitted', 'email_templates/test', to=['gzhou@records.nyc.gov'])
            return api_response.success({
                "document": doc.as_dict(),
                "success_message": {
                    "text": "Your publication has been submitted for approval."
                }
            })
        return api_response.fail(errors)

    @login_required
    def patch(self, doc_id):
        # TODO: edits once document is created
        pass
