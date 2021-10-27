from flask import render_template, request, Blueprint, flash, redirect, url_for
from app.profile.forms import ChangePasswordForm, ChangeEmailForm
from app.models import User, Order, Day
from flask_login import login_required, current_user
from app import bcrypt, db

prof = Blueprint('profile', __name__)


@prof.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user, title="Профиль")


@prof.route('/change_master_password', methods=['GET', 'POST'])
@login_required
def change_master_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if bcrypt.check_password_hash(user.password, form.current_password.data) and form.current_password.data != form.new_password.data:
            user.password = bcrypt.generate_password_hash(
                form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Пароль успешно сменен!', "success")
            return redirect(url_for('profile.profile'))
        else:
            flash('Мастер-пароль введен неверно и/или пароли совпадают')
            return redirect(url_for('profile.change_master_password'))
    return render_template('profile/change_master_password.html', form=form, title="Смена пароля")


@prof.route("/changeemail", methods=["GET", "POST"])
@login_required
def changeemail():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.master_password.data):
            flash("Неправильный пароль")
            return redirect(url_for("profile.changeemail"))
        current_user.change_email(form.new_email.data)
        db.session.commit()
        flash("Почта успешно сменена!")
        return redirect(url_for('profile.profile'))
    return render_template('profile/changeemail.html', form=form, title="Смена почты")


@prof.route("/uorder/<int:id>/delete")
@login_required
def delete_uorder(id):
    order = Order.query.filter_by(id=int(id)).first()
    day = Day.query.filter_by(date=order.date).first()
    day.orders_amount += order.amount
    db.session.delete(order)
    db.session.commit()
    flash("Заявка успешно удалена!")
    return redirect(url_for('profile.profile'))
