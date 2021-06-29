from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from source import db
from source.admin_panel_models import Admin
from source.admins.forms import AdminRegisterForm, AdminLoginForm, AdminUpdateForm
from werkzeug.security import generate_password_hash

admins_blueprint = Blueprint('admins', __name__, template_folder='templates')


# register_managers
@admins_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = AdminRegisterForm()

    if form.validate_on_submit():
        new_admin = Admin(email=form.email.data,
                          name=form.name.data,
                          password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admins.login'))

    return render_template('admin_register.html', form=form)


# login
@admins_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        cur_admin = Admin.query.filter_by(email=form.email.data).first()
        if cur_admin and cur_admin.check_password(form.password.data):
            login_user(cur_admin)
            flash('login success')

            next = request.args.get('next')

            if next is None or next[0] == '/admin_panel':
                next = url_for('admins.admin')
            return redirect(next)

    return render_template('admin_login.html', form=form)


# logout
@admins_blueprint.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash('logout success!')
    return redirect(url_for('admin_panel.main'))


# admin page (update)
@admins_blueprint.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    form = AdminUpdateForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('update success')

    elif request.method == "GET":
        form.email.data = current_user.email
        form.name.data = current_user.name

    return render_template('admin.html', current_user=current_user, form=form)
