from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from source.admin_panel_models import TaskType


class ButtonAddForm(FlaskForm):
    add = SubmitField(' ')


class ButtonAddWordForm(FlaskForm):
    add_word = SubmitField(' ')


class ButtonAddGrammarForm(FlaskForm):
    add_grammar = SubmitField(' ')


class ButtonDeleteForm(FlaskForm):
    delete = SubmitField(' ')


class NameForm(FlaskForm):
    name = StringField('name')
    update = SubmitField('update')


class RightSentForm(FlaskForm):
    sent_char_A = StringField('sent_char_A')
    sent_pinyin_A = StringField('sent_pinyin_A')
    sent_lang_A = StringField('sent_lang_A')
    sent_lit_A = StringField('sent_lit_A')
    sent_char_B = StringField('sent_char_B')
    sent_pinyin_B = StringField('sent_pinyin_B')
    sent_lang_B = StringField('sent_lang_B')
    sent_lit_B = StringField('sent_lit_B')
    submit = SubmitField('submit')


class WrongSentForm(FlaskForm):
    sent_char = StringField('sent_char_A')
    sent_pinyin = StringField('sent_pinyin_A')
    sent_lang = StringField('sent_lang_A')
    submit = SubmitField('submit')


class UploadImageForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(['png', 'jpg', 'svg'])])
    upload = SubmitField('upload')


class SelectTaskTypeForm(FlaskForm):
    choices = [(_type.id, f'{_type.id}) {_type.name}') for _type in TaskType.query.all()]
    type = SelectField('select task type', choices=choices)
    add = SubmitField(' ')


class BackButtonForm(FlaskForm):
    back = SubmitField(' ')


class UploadVideoForm(FlaskForm):
    video = FileField('video', validators=[FileAllowed(['mp4'])])
    upload = SubmitField('upload')

class UploadSentAAudioForm(FlaskForm):
    sent_A_audio = FileField('audio', validators=[FileAllowed(['mp3'])])
    upload_sent_A_audio = SubmitField('upload')
