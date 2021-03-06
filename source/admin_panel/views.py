from flask import Blueprint, render_template

admin_panel_blueprint = Blueprint('admin_panel', __name__, url_prefix='/admin_panel', template_folder='templates')


@admin_panel_blueprint.route('/')
@admin_panel_blueprint.route('/admin')
def main():
    return render_template('main.html')

