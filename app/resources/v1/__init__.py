from .auth.api import AuthAPI as Auth
from .document.api import DocumentAPI as Document
from .upload.api import UploadAPI as Upload
from .subjects.api import SubjectsAPI as Subjects
from .report_types.api import ReportTypesAPI as ReportTypes
from .languages.api import LanguagesAPI as Languages

from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint('1.0', __name__)
api = Api(blueprint)
