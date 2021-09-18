from flask import render_template, url_for, flash, redirect, Blueprint, request
from app.models import User
from app.auth.forms import (LoginForm, RegistrationForm,
                            SendResetPasswordForm, ResetPasswordForm)
from flask_login import login_user, logout_user, current_user, login_required
from app import db, bcrypt
from app.auth.email import reset_email
auth = Blueprint("auth", __name__)


@auth.route('/sign in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Неправильное имя пользователя и/или пароль!")
            return redirect(url_for("auth.sign_in"))
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for("main.index"))
    return render_template('auth/login.html', form=form, title="Авторизация")


@auth.route('/sign up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if form.validate_on_submit():
        u_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=u_password)
        db.session.add(user)
        db.session.commit()
        flash("Приветствуем нового пользователя!", "success")
        return redirect(url_for("auth.sign_in"))
    return render_template('auth/register.html', form=form, title='Регистрация')


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/reset_password", methods=['GET', 'POST'])
def send_reset_password_email():
    form = SendResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            reset_email(user)
            flash("Следуйте инструкциям на почте для восстановления пароля")
            return redirect(url_for("auth.sign_in"))
        else:
            flash("Пользователь с такой почтой не найден!")
            return redirect(url_for("auth.sign_in"))
    return render_template('email/send_reset_password_email.html', form=form, title="Сброс пароля")


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for("auth.sign_in"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(
            password=bcrypt.generate_password_hash(
                form.new_password.data)
        )
        db.session.commit()
        flash("Пароль успешно сменен!")
        return redirect(url_for("auth.sign_in"))
    return render_template('email/reset_password.html', form=form, title="Сброс пароля")
