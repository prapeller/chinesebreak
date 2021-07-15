from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from source.admin_panel_models import TaskType


class ButtonAddForm(FlaskForm):
    add = SubmitField(' ')


class ButtonDeleteForm(FlaskForm):
    delete = SubmitField(' ')


class NameForm(FlaskForm):
    name = StringField('name')
    update = SubmitField('update')


class UploadImageForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(['png', 'jpg', 'svg'])])
    upload = SubmitField('upload')


class SelectTaskTypeForm(FlaskForm):
    choices = [(_type.id, f'{_type.id}) {_type.name}') for _type in TaskType.query.all()]
    type = SelectField('select task type', choices=choices)
    add = SubmitField(' ')


# class ButtonSelectForm(FlaskForm):
#     select = SubmitField(' ')