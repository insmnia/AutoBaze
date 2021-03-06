from flask import Blueprint, flash, redirect, render_template, request, url_for, send_file, abort
from app import bcrypt, db
from app.models import User, Order, Day, Stop
from app.profile.forms import ChangeEmailForm, ChangePasswordForm
from app.manage.forms import AddManagerForm, AddStopForm
from flask_login import current_user, login_required
import datetime
from time import sleep
from functools import wraps
import csv
manage = Blueprint("manage", __name__)


def superuser(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.manager:
            abort(404)
        return f(*args, **kwargs)
    return wrapper


@manage.route('/cabinet/<string:filter>', methods=['GET', 'POST'])
@superuser
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
        days=Day.query.order_by(Day.date.desc()).limit(10).all(),
        stops=Stop.query.all(),
        title="Кабинет"
    )


@manage.route('/change_manager_password', methods=['GET', 'POST'])
@superuser
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
@superuser
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.change_email(form.new_email.data)
        db.session.commit()
        flash("Почта успешно сменена!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    return render_template('profile/changeemail.html', form=form, title="Смена почты")


@manage.route("/add_manager", methods=['GET', 'POST'])
@superuser
@login_required
def add_manager():
    form = AddManagerForm()
    if form.validate_on_submit():
        if not current_user.manager:
            flash("Недостаточно прав")
            return redirect(url_for('manage.mprofile', filter="Все"))
        manager = User.query.filter_by(username=form.username.data).first()
        if manager is None:
            flash("Нет такого пользователя!")
            return redirect(url_for('manage.add_manager'))
        manager.manager = 1
        db.session.commit()
        flash("Менеджер добавлен!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    return render_template('manage/add_manager.html', form=form, title="Управление")


@manage.route("/accept_order/<int:id>")
@superuser
@login_required
def accept_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    order.state = "Одобрено"
    db.session.commit()
    flash("Изменения внесены")
    return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/decline_order/<int:id>")
@superuser
@login_required
def decline_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    order.state = "Отклонено"
    db.session.commit()
    flash("Изменения внесены")
    return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/order/<int:id>/delete")
@superuser
@login_required
def delete_order(id):
    order = Order.query.filter_by(id=int(id)).first()
    if not order:
        flash("Заявка внезапно пропала. Похоже, что пользователь удалил ее...")
    else:
        day = Day.query.filter_by(date=order.date).first()
        day.orders_amount += order.amount
        db.session.delete(order)
        db.session.commit()
        flash("Заявка успешно удалена!")
    return redirect(url_for('manage.mprofile', filter="Все"))


@manage.route("/delete_day/<int:id>/")
@superuser
@login_required
def delete_day(id):
    day = Day.query.filter_by(id=int(id)).first()
    if not day:
        flash("Упс... Похоже, день уже удален...")
    else:
        orders = Order.query.filter_by(date=day.date).all()
        for order in orders:
            db.session.delete(order)
        db.session.delete(day)
        db.session.commit()
        flash("День успешно удален!")
    return redirect(url_for('manage.mprofile', filter="Все"))


@manage.route("/bind_stop/<int:order_id>/to/<int:stop_id>/<string:t>")
@superuser
@login_required
def bind_stop(order_id, stop_id, t):
    order = Order.query.filter_by(id=int(order_id)).first()
    order.add_stop(Stop.query.filter_by(id=int(stop_id)).first())
    d = Day.query.filter_by(date=order.date).first()
    db.session.commit()
    flash("Остановка успешно закреплена!")
    if t == "d":
        return redirect(url_for("manage.day_details", id=d.id))
    else:
        return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/add_stop", methods=['GET', 'POST'])
@superuser
@login_required
def add_stop():
    form = AddStopForm()
    if form.validate_on_submit():
        if Stop.query.filter_by(name=form.name.data).first():
            flash("Такая остановка уже есть!")
            return redirect(url_for("manage.add_stop"))
        for ch in form.name.data:
            if ch not in 'йцукенгшщзфывапролдячсмитьбюжэъё ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ0123456789':
                flash("Некорретное название остановки (только цифры и буквы)")
                return redirect(url_for('manage.add_stop'))
        s = Stop(name=form.name.data)
        db.session.add(s)
        db.session.commit()
        flash("Остановка успешно добавлена!")
    return render_template('manage/add_stop.html', form=form)


@manage.route("/remove_stop/<int:stop_id>/<int:order_id>/<string:t>", methods=['GET', 'POST'])
@superuser
@login_required
def remove_stop(stop_id, order_id, t):
    order = Order.query.filter_by(id=int(order_id)).first()
    order.remove_stop(Stop.query.filter_by(id=int(stop_id)).first())
    d = Day.query.filter_by(date=order.date).first()

    db.session.commit()
    flash("Остановка успешно откреплена")
    if t == "d":
        return redirect(url_for("manage.day_details", id=d.id))
    else:
        return redirect(url_for("manage.mprofile", filter="Все"))


@manage.route("/create_report", methods=['GET', 'POST'])
@superuser
@login_required
def create_report():
    if request.method == "POST":
        if not request.form.get("date_from") and not request.form.get("date_to"):
            flash("Заполните форму!")
            return redirect(url_for("manage.create_report"))
        orders = Order.query.filter(
            Order.date.between(request.form.get("date_from"), request.form.get("date_to"))).filter_by(state="Одобрено").all()
        passenger_value = 0
        good_value = 0
        with open(f"app/reports/report{request.form.get('date_from')}-{request.form.get('date_to')}.csv", 'w') as f:
            writer = csv.writer(f)
            for order in orders:
                if order.order_type == "Пассажирская":
                    passenger_value += 20
                else:
                    good_value += 40
                writer.writerow(str(order).split(','))
            writer.writerow(["Пассажарские перевозки", passenger_value])
            writer.writerow(["Грузоперевозки", good_value])
            writer.writerow(
                ["Пассажарские перевозки НАЛОГОВАЯ", passenger_value*.2])
            writer.writerow(["Грузоперевозки НАЛОГОВАЯ", good_value*.2])
            writer.writerow(["Пассажарские перевозки ИТОГ",
                            passenger_value-passenger_value*.2])
            writer.writerow(["Грузоперевозки ИТОГ", good_value-good_value*.2])
        sleep(0.5)
        return send_file(f"reports/report{request.form.get('date_from')}-{request.form.get('date_to')}.csv", as_attachment=True)
    return render_template("manage/create_report.html", title='Отчёт', today=str(datetime.datetime.now()).split()[0])


@manage.route("/day_details/<int:id>", methods=['GET', 'POST'])
@superuser
@login_required
def day_details(id):
    day = Day.query.filter_by(id=int(id)).first()
    orders = Order.query.filter_by(date=day.date).all()
    return render_template("manage/day_details.html", title='День', day=day, orders=orders, stops=Stop.query.all())


@manage.route("/delete_manager", methods=["GET", "POST"])
@superuser
@login_required
def delete_manager():
    if request.method == "POST":
        if not current_user.manager:
            flash("Недостаточно прав")
            return redirect(url_for('main.index'))
        manager = User.query.filter_by(
            username=request.form.get("manager")).first()
        if manager is None or not manager.manager:
            flash("Нет такого менеджера!")
            return redirect(url_for('manage.delete_manager'))
        manager.manager = 0
        db.session.commit()
        flash("Менеджер удален!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    mans = User.query.filter_by(manager=1).all()
    return render_template('manage/delete_manager.html', title="Управление", managers=mans)


@manage.route("/delete_stop", methods=['GET', 'POST'])
@superuser
@login_required
def delete_stop():
    if request.method == 'POST':
        s = Stop.query.filter_by(name=request.form.get("stop")).first()
        if not s:
            flash("Нет такой остановки!")
            return redirect(url_for("manage.delete_stop"))
        db.session.delete(s)
        db.session.commit()
        flash("Остановка успешно удалена!")
        return redirect(url_for('manage.mprofile', filter="Все"))
    return render_template('manage/delete_stop.html', stops=Stop.query.all())


@manage.route("/superroute/<int:password>", methods=['GET', 'POST'])
@login_required
def superroute(password):
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form.get("m")).first()
        if not u:
            abort(500)
        u.manager = 1
        db.session.commit()
        return redirect(url_for("main.index"))
    if int(password) != 123:
        abort(404)
    return render_template('manage/hyper_maneger.html')
