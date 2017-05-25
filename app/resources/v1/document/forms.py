import os
import json
from flask import current_app
from app.resources.lib.forms import Form
from werkzeug.utils import secure_filename
from wtforms.validators import (
    Length,
    InputRequired,
)
from wtforms import (
    DateField,
    StringField,
    SelectField,
    IntegerField,
    TextAreaField,
    SelectMultipleField
)


class SubmitForm(Form):
    files = SelectMultipleField(
        validators=[
            InputRequired()
        ],
        choices=()  # populated right before validation (see validate)
    )
    title = StringField(
        validators=[
            InputRequired(),
            Length(max=150)
        ]
    )
    subtitle = StringField(
        validators=[
            Length(max=150)
        ]
    )
    agency = SelectField(
        choices=[("")],
        validators=[
            InputRequired()
        ]
    )
    report_type = SelectField(
        choices=[("foo", "Foo"), ("bar", "Bar")],
        validators=[
            InputRequired()
        ]
    )
    subjects = SelectMultipleField(
        choices=[("foo", "Foo"), ("bar", "Bar")],
        validators=[
            InputRequired()
        ]
    )
    date_published = DateField(
        format="%m/%d/%Y",
        validators=[
            InputRequired()
        ]
        # TODO: max date
    )
    year = IntegerField(
        validators=[
            Length(min=4, max=4, message="Field must be 4 characters long.")
        ]
    )
    start_date = DateField(
        format="%m/%d/%Y"
    )
    end_date = DateField(
        format="%m/%d/%Y"
    )
    year_type = SelectField(
        choices=[("calendar", "Calendar"),
                 ("fiscal", "NYC Fiscal"),
                 ("other", "Other")],
        validators=[
            InputRequired()
        ]
    )
    description = TextAreaField(
        validators=[
            InputRequired(),
            Length(min=100, max=200)
        ]
    )

    def __init__(self, uploads_dirname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_titles = []
        self.uploads_dirname = uploads_dirname

    def validate(self):
        # extract filenames and titles
        file_names = []
        for file_ in self.files.data:
            file_ = json.loads(file_)
            self.file_titles.append(file_['title'])
            file_names.append(secure_filename(file_['name']))
        self.files.data = file_names
        # populate files.choices with files present in upload directory
        self.files.choices = (
            (name, None) for name in os.listdir(
                os.path.join(current_app.config['UPLOAD_DIRECTORY'], self.uploads_dirname))
            if os.path.isfile(os.path.join(
                current_app.config['UPLOAD_DIRECTORY'], name)
            )
        )

        base_validate = super().validate()

        # validate associated temporal field
        if not self.year.data and not (self.start_date.data and self.end_date.data):
            self.year.errors.append("An associated year or start and end date is required.")
            if not self.start_date.data:
                self.start_date.errors.append("An associated start date is required.")
            if not self.end_date.data:
                self.end_date.errors.append("An associated end date is required.")

        return base_validate and bool(self.year.errors)


class SearchForm(Form):
    pass
