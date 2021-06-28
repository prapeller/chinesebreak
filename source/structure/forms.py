from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from source.admin_panel_models import TaskType


class ButtonAddForm(FlaskForm):
    add = SubmitField('ADD')


class ButtonDeleteForm(FlaskForm):
    delete = SubmitField('DELETE')


class NameForm(FlaskForm):
    name = StringField('name')
    update = SubmitField('update')


class TopicImageForm(FlaskForm):
    image = FileField('image', validators=[FileAllowed(['png', 'jpg', 'svg'])])
    update = SubmitField('upload')


class SelectTaskTypeForm(FlaskForm):
    choices = [(_type.id, f'{_type.id}) {_type.name}') for _type in TaskType.query.all()]
    type = SelectField('select task type', choices=choices)
    add = SubmitField('ADD')
