from flask import Flask, render_template, url_for, redirect, Blueprint

elements_blueprint = Blueprint('elements', __name__, template_folder='templates/elements')
