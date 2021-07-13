from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, SubmitField, SelectField, FileField
from source.admin_panel_models import TaskType


class ButtonAddForm(FlaskForm):
    add = SubmitField(' ')


class ButtonDeleteForm(FlaskForm):
    delete = SubmitField(' ')


class NameForm(FlaskForm):
    name = StringField('name')
    update = SubmitField('update')


class SearchForm(Form):
    search = StringField('search')


class WordForm(Form):
    pinyin = StringField('pinyin')
    character = StringField('character')
    lang = StringField('lang')
    lit = StringField('lit')


class UploadImageForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(['png', 'jpg', 'svg'])])
    upload = SubmitField('upload')


class UploadAudioForm(FlaskForm):
    audio = FileField('audio', validators=[FileAllowed(['mp3', 'mp4'])])
    upload = SubmitField('upload')
