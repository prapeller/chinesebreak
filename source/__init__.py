import os, sys
import sqlite3

from sqlalchemy import engine
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
# conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db.sqlite'))
# cursor = conn.cursor()
# cursor.execute("""
# create table task_types (id SERIAL primary key, name VARCHAR(50));
# """)
# cursor.execute("""
# insert into task_types
# values (1, 'word_image'),
#        (2, 'word_char_from_lang'),
#        (3, 'word_lang_from_char'),
#        (4, 'word_char_from_video'),
#        (5, 'word_match'),
#        (6, 'sent_image'),
#        (7, 'sent_char_from_lang'),
#        (8, 'sent_lang_from_char'),
#        (9, 'sent_lang_from_video'),
#        (10, 'sent_say_from_char'),
#        (11, 'sent_say_from_video'),
#        (12, 'sent_paste_from_char'),
#        (13, 'sent_choose_from_char'),
#        (14, 'sent_delete_from_char'),
#        (15, 'dialog_A_char_from_char'),
#        (16, 'dialog_B_char_from_video'),
#        (17, 'dialog_A_puzzle_char_from_char'),
#        (18, 'dialog_B_puzzle_char_from_char'),
#        (19, 'puzzle_char_from_lang'),
#        (20, 'puzzle_lang_from_char'),
#        (21, 'puzzle_char_from_video'),
#        (22, 'draw_character');
# """)

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

from source.structure.task_1_view import task_1_bp
from source.structure.task_2_view import task_2_bp
from source.structure.task_3_view import task_3_bp
from source.structure.task_4_view import task_4_bp
from source.structure.task_5_view import task_5_bp
from source.structure.task_6_view import task_6_bp

app.register_blueprint(admin_panel_blueprint)
app.register_blueprint(admins_blueprint)
app.register_blueprint(structure_blueprint)
app.register_blueprint(elements_blueprint)
app.register_blueprint(task_1_bp)
app.register_blueprint(task_2_bp)
app.register_blueprint(task_3_bp)
app.register_blueprint(task_4_bp)
app.register_blueprint(task_5_bp)
app.register_blueprint(task_6_bp)


