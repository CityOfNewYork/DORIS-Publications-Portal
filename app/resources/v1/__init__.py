from .publication.api import PublicationAPI as Publication
from .upload.api import UploadAPI as Upload

from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint('1.0', __name__)
api = Api(blueprint)
