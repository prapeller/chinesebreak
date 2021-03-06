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
from source.structure.task_7_view import task_7_bp
from source.structure.task_8_view import task_8_bp
from source.structure.task_9_view import task_9_bp
from source.structure.task_10_view import task_10_bp
from source.structure.task_11_view import task_11_bp
from source.structure.task_12_view import task_12_bp
from source.structure.task_13_view import task_13_bp
from source.structure.task_14_view import task_14_bp
from source.structure.task_15_view import task_15_bp
from source.structure.task_16_view import task_16_bp
from source.structure.task_17_view import task_17_bp
from source.structure.task_18_view import task_18_bp
from source.structure.task_19_view import task_19_bp
from source.structure.task_20_view import task_20_bp
from source.structure.task_21_view import task_21_bp
from source.structure.task_22_view import task_22_bp
from source.structure.task_23_view import task_23_bp

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
app.register_blueprint(task_7_bp)
app.register_blueprint(task_8_bp)
app.register_blueprint(task_9_bp)
app.register_blueprint(task_10_bp)
app.register_blueprint(task_11_bp)
app.register_blueprint(task_12_bp)
app.register_blueprint(task_13_bp)
app.register_blueprint(task_14_bp)
app.register_blueprint(task_15_bp)
app.register_blueprint(task_16_bp)
app.register_blueprint(task_17_bp)
app.register_blueprint(task_18_bp)
app.register_blueprint(task_19_bp)
app.register_blueprint(task_20_bp)
app.register_blueprint(task_21_bp)
app.register_blueprint(task_22_bp)
app.register_blueprint(task_23_bp)
