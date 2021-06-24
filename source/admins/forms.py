from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from source.admin_panel_models import Admin
from wtforms import ValidationError
from flask import flash


class AdminRegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message='fill in!'), Email(message='should be email!')])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('cnf_password', 'passwords should match')])
    cnf_password = PasswordField('confirm password', validators=[DataRequired()])  #
    submit = SubmitField('register')

    def validate_email(self, email):
        if Admin.query.filter_by(email=email.data).first():
            flash('email already exist', 'info')
            raise ValidationError('email already used')


class AdminLoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    submit = SubmitField('login')


class AdminUpdateForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('cnf_password', 'passwords should match')])
    cnf_password = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('update')

