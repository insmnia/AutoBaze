from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_app import bcrypt, db
from flask_app.models import User, Order, Day, Stop
from flask_app.profile.forms import ChangeEmailForm, ChangePasswordForm
from flask_app.manage.forms import AddManagerForm, AddStopForm
from flask_login import current_user, login_required

manage = Blueprint("manage", __name__)


@manage.route('/cabinet/<string:filter>', methods=['GET', 'POST'])
@login_required
def mprofile(filter):
    if filter == "Все":
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(state=filter).all()
    return render_template(
        'manage/manager_profile.html',
        user=current_user,
        orders=orders,
        days=Day.query.all(),
        stops=Stop.query.all(),
        title="Кабинет"
    )


@manage.route('/change_manager_password', methods=['GET', 'POST'])
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
            return redirect(url_for('manage.mprofile', filter="Все"))
        else:
            flash('Мастер-пароль введен неверно и/или пароли совпадают')
            return redirect(url_for('manage.change_master_password'))
    return render_template('profile/change_master_password.html', form=form, title="Смена пароля")


@manage.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.change_email(form.new_email.data)
        db.session.commit()
        flash("Почта успешно сменена!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    return render_template('profile/change_email.html', form=form, title="Смена почты")


@manage.route("/add_manager", methods=['GET', 'POST'])
@login_required
def add_manager():
    form = AddManagerForm()
    if form.validate_on_submit():
        print(current_user)
        if not current_user.manager:
            flash("Недостаточно прав")
            return redirect(url_for('manage.mprofile', filter="Все"))
        manager = User.query.filter_by(username=form.username.data).first()
        if manager is None:
            flash("Нет такого пользователя!")
            return redirect(url_for('manage.mprofile', filter="Все"))
        manager.manager = 1
        db.session.commit()
        flash("Менеджер добавлен!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    return render_template('manage/add_manager.html', form=form, title="Управление")


@manage.route("/accept_order/<int:id>")
@login_required
def accept_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    order.state = "Одобрено"
    db.session.commit()
    flash("Изменения внесены")
    return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/decline_order/<int:id>")
@login_required
def decline_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    order.state = "Отклонено"
    db.session.commit()
    flash("Изменения внесены")
    return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/order/<int:id>/delete")
@login_required
def delete_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    day = Day.query.filter_by(date=order.date).first()
    day += order.amount
    db.session.delete(order)
    db.session.commit()
    flash("Заявка успешно удалена!")
    return redirect(url_for('manage.mprofile', filter="Все"))


@manage.route("/delete_day/<int:id>/")
@login_required
def delete_day(id):
    day = Day.query.filter_by(id=int(id)).first()
    orders = Order.query.filter_by(date=day.date).all()
    db.session.delete(*orders)
    db.session.delete(day)
    db.session.commit()
    flash("День успешно удален!")
    return redirect(url_for('manage.mprofile', filter="Все"))


@manage.route("/bind_stop/<int:order_id>/to/<int:stop_id>")
@login_required
def bind_stop(order_id, stop_id):
    order = Order.query.filter_by(id=int(order_id)).first()
    order.add_stop(Stop.query.filter_by(id=int(stop_id)).first())
    db.session.commit()
    flash("Остановка успешно закреплена!")
    return redirect(url_for('manage.detailed_order', id=order.id))


@manage.route("/add_stop", methods=['GET', 'POST'])
@login_required
def add_stop():
    form = AddStopForm()
    if form.validate_on_submit():
        s = Stop(name=form.name.data)
        db.session.add(s)
        db.session.commit()
        flash("Остановка успешно добавлена!")
    return render_template('manage/add_stop.html', form=form)


@manage.route("/details/order/<int:id>", methods=['GET', 'POST'])
def detailed_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    return render_template('manage/order_detailed.html', order=order, stops=Stop.query.all())


@manage.route("/remove_stop/<int:stop_id>/<int:order_id>", methods=['GET', 'POST'])
@login_required
def remove_stop(stop_id, order_id):
    order = Order.query.filter_by(id=int(order_id)).first()
    order.remove_stop(Stop.query.filter_by(id=int(stop_id)).first())
    db.session.commit()
    flash("Остановка успешно удалена")
    return redirect(url_for("manage.detailed_order", id=order.id))

# TODO отчёт


@manage.route("/create_report", methods=['GET', 'POST'])
@login_required
def create_report():
    if request.method == "POST":
        date_from = datetime.date(
            *map(int, request.form.get("date_from").split('-')))
        date_to = datetime.date(
            *map(int, request.form.get("date_to").split('-')))
    return render_template("manage/create_report.html")
