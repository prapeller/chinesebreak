from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, SubmitField, SelectField, FileField
from source.admin_panel_models import TaskType


class ButtonAddForm(FlaskForm):
    add = SubmitField('ADD')


class ButtonDeleteForm(FlaskForm):
    delete = SubmitField('DELETE')


class NameForm(FlaskForm):
    name = StringField('name')
    update = SubmitField('update')


class SearchForm(Form):
    search = StringField('search')