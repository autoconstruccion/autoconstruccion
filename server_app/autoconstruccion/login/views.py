from flask import Blueprint, current_app, redirect, abort
from flask import request, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user
import itsdangerous
from autoconstruccion.models import db, User
from .forms import LoginForm, RegisterForm

bp = Blueprint('login', __name__)


# This file must be imported inside an app context
serializer = itsdangerous.URLSafeSerializer(secret_key=current_app.config['SECRET_KEY'])
ACTIVATION_SALT = current_app.config['USER_ACTIVATION_SALT']


def get_activation_link(user):
    return url_for('activate', code=serializer.dumps(user.user_id, salt=ACTIVATION_SALT))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():

        # test duplication of user mail -> make in a better way in future, form validator
        user = User.query.filter_by(email=register_form.email.data).one_or_none()
        if user:
            flash('email already in use by another user.', 'error')
            register_form.email.errors.append('email already in use by another user.')
            return render_template('register.html', register_form=register_form)

        new_user = User()
        register_form.populate_obj(new_user)
        new_user.store_password_hashed(register_form.password.data)

        # send activation email

        # new user is all right, persist
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully.', 'success')
        # redirect to user data fill....
        return redirect(url_for('web.index'))

    flash('Please correct the required fields.', 'error')
    return render_template('register.html', register_form=register_form)


def next_is_valid(next_url):
    # Exclude some urls here -> return False
    return True


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        # Return one user filter by email or None. Raise an exception if more than one user is find.
        user = User.query.filter_by(email=login_form.email.data).one_or_none()
        if not (user and user.test_password(login_form.password.data)):
            flash('Incorrect user email or password.', 'error')
            return render_template('login_sign.html', login_form=login_form, register_form=register_form)

        login_user(user)
        flash('Logged in successfully.', 'success')

        next_url = request.args.get('next')
        # next_is_valid should check if the user has valid permission to access the `next` url
        if not next_is_valid(next_url):
            return abort(400)

        return redirect(next_url or url_for('web.index'))
    return render_template('login_sign.html', login_form=login_form, register_form=register_form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@bp.route('/activate/<code>')
def activate(code):
    try:
        user_id = serializer.loads(code, salt=ACTIVATION_SALT)
    except itsdangerous.BadSignature:
        abort(404)
    # user is find, activate it
    user = db.session.query(User).get(user_id)
    user.activate()
    db.session.commit()
