import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# app and configs:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'topsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
