from .auth.api import AuthAPI as Auth
from .document.api import DocumentAPI as Document
from .upload.api import UploadAPI as Upload
from .subjects.api import SubjectsAPI as Subject
from .report_types.api import ReportTypesAPI as ReportTypes

from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint('1.0', __name__)
api = Api(blueprint)
