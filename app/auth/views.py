# coding=utf-8
from flask import render_template, request, flash, redirect, url_for
from . import auth
from .forms import LoginForm
from ..models import User
from .. import db
from flask_login import login_user, logout_user, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is not None:
            if user.username == 'admin':
                login_user(user)
                return redirect(url_for('admin.adminhome'))
            else:
                login_user(user)
                return redirect(url_for('main.userhome'))
        else:
            flash('用户名或密码错误.')

    return render_template('login.html',
                           title=u'登录',
                           form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
