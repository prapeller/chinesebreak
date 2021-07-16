import os, sys

import flask_sijax
from flask import Flask, g, render_template, url_for, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

# app and configs:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'topsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# add sijax
app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax')
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

# db setup:
db = SQLAlchemy(app)
Migrate(app, db)

# login manager configs:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admins.login' or 'users.login'
login_manager.login_message = 'to access this page you should login'
login_manager.login_message_category = 'info'

# blueprints setup:
from source.admin_panel.views import admin_panel_blueprint
from source.admins.views import admins_blueprint
from source.structure.views import structure_blueprint
from source.elements.views import elements_blueprint

app.register_blueprint(admin_panel_blueprint)
app.register_blueprint(admins_blueprint)
app.register_blueprint(structure_blueprint)
app.register_blueprint(elements_blueprint)

