from flask import Blueprint, render_template

admin_panel_blueprint = Blueprint('admin_panel', __name__, template_folder='templates')


@admin_panel_blueprint.route('/')
def main():
    return render_template('main.html')


@admin_panel_blueprint.route('/admin_panel/info')
def info():
    return render_template('info.html')


