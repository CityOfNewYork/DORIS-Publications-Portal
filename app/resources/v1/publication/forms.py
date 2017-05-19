import os
from flask import current_app
from app.resources.lib.forms import Form
from werkzeug.utils import secure_filename
from wtforms.validators import (
    Length,
    InputRequired,
)
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SelectMultipleField
)


class SubmitForm(Form):
    filenames = SelectMultipleField(
        validators=[
            InputRequired()
        ],
        choices=()  # populated right before validation
    )
    title = StringField(
        validators=[
            InputRequired(),
            Length(max=10)
        ]
    )
    type = SelectField(
        choices=[("foo", "Foo"), ("bar", "Bar")],
        validators=[
            InputRequired()
        ]
    )
    description = TextAreaField(
        validators=[
            InputRequired()
        ]
    )

    def validate(self):  # TODO: change to deal with parent dir and make sure all choices (and only those choices) are true
        # convert file names to secure variants
        self.filenames.data = [
            secure_filename(name) for name in self.filenames.data
        ]
        # populate filenames.choices
        self.filenames.choices = (
            (name, None) for name in os.listdir(current_app.config['UPLOAD_DIRECTORY'])
            if os.path.isfile(os.path.join(
                current_app.config['UPLOAD_DIRECTORY'], name)
            )
        )
        return super(SubmitForm, self).validate()


class SearchForm(Form):
    pass
