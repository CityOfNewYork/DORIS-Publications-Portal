from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import InputRequired


class SearchForm(Form):
    user_input = StringField(validators =[InputRequired()])