from atexit import register
from flask import (Blueprint, 
                   render_template,
                   redirect,
                   url_for,
                   flash,
                   g,
                   session,
                   request)

from malonekeep.forms.auth_form import LoginForm, RegisterForm
from malonekeep.models.user import User as UserModel
from werkzeug import security

NAME = 'auth'

bp = Blueprint(NAME, __name__, url_prefix='/auth')


@bp.before_app_request
def before_app_request():
    g.user = None
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            g.user = user
        else:
            session.pop('user_id', None)
        

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        password = form.data.get('password')
        user = UserModel.find_one_by_user_id(user_id)
        

        if user:
            if security.check_password_hash(user.password, password):
                session['user_id'] = user_id
                return redirect(url_for('base.index'))
            else:
                flash("패스워드 틀렸음")
                return redirect(request.path)
        else:
            flash("유저가 없음")
    else:
        flash_form_error(form)
    return render_template(f'{NAME}/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        user = UserModel.find_one_by_user_id(user_id)

        if user:
            flash('유져 있음 다른아이디로 하셈')
        else:
            user = UserModel(
                user_id = user_id,
                user_name = form.data.get('user_name'),
                password = security.generate_password_hash(form.data.get('password'))
            )
            g.db.add(user)
            g.db.commit()
            session['user_id'] = user_id
            return redirect(url_for('base.index'))
    else:
        flash_form_error(form)
    return render_template(f'{NAME}/register.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('base.index'))


def flash_form_error(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)