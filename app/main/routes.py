import datetime
from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Order, Day
import re
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    allowed_symbols = 'йцукенгшщзфывапролдячсмитьбюжэъё ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
    if request.method == "POST":

        Fcs = request.form.get("FCS")
        Fcs = re.sub('\s+', ' ', Fcs)
        for ch in Fcs:
            if ch not in allowed_symbols:
                flash('Некорретное имя')
                return redirect(url_for('main.index'))
        if all([x == ' ' for x in Fcs]):
            flash('Некорректное имя')
            return redirect(url_for('main.index'))

        phone = request.form.get("phone")
        email = request.form.get("email")

        departure_point = request.form.get("from")
        departure_point = re.sub('\s+', ' ', departure_point)
        if not departure_point:
            flash('Некорректное место отправки')
            return redirect(url_for('main.index'))
        for ch in departure_point:
            if ch not in allowed_symbols + '0123456789':
                flash('Некорректное место отправки')
                return redirect(url_for('main.index'))

        arrival_point = request.form.get("to")
        arrival_point = re.sub('\s+', ' ', arrival_point)
        if not arrival_point:
            flash('Некорректное место отправки')
            return redirect(url_for('main.index'))
        for ch in arrival_point:
            if ch not in allowed_symbols+'0123456789':
                flash('Некорректное место отправки')
                return redirect(url_for('main.index'))

        amount = request.form.get("amount")
        auto = request.form.get("auto")
        if request.form.get("ta") == "2":
            amount = 20
        if not all([Fcs, phone, email, departure_point, arrival_point, amount, auto]):
            flash("Заполните форму полностью!")
            return redirect(url_for('main.index'))

        date = request.form.get("calendar").split('-')
        date = datetime.date(*map(int, date))
        day = Day.query.filter_by(date=date).first()

        if day is None:
            day = Day(
                date=date, orders_amount=current_app.config['ORDERS_AMOUNT'])
            db.session.add(day)

        if request.form.get("ta") == "1":
            if day.orders_amount - int(amount) < 0:
                flash("На этот день нет столько мест!")
                return redirect(url_for('main.index'))
            else:
                day.orders_amount -= int(amount)
        else:
            if day.orders_amount < 20:
                flash("Невозможно выполнить грузоперевозку в этот день!")
                return redirect(url_for('main.index'))
            else:
                day.orders_amount -= 20

        order = Order(
            FCs=Fcs,
            phone=phone,
            email=email,
            departure_point=departure_point,
            arrival_point=arrival_point,
            order_type=["Пассажирская",
                        "Грузоперевозка"][request.form.get("ta") != "1"],
            amount=amount,
            state="В обработке",
            creator=current_user.id,
            date=date,
            auto=auto
        )
        db.session.add(order)
        db.session.commit()
        flash("Заявка успешно отправлена! Ожидайте обратной связи")
    today = str(datetime.datetime.now()).split()[0]
    max_day = str(datetime.datetime.now() +
                  datetime.timedelta(days=7)).split()[0]
    return render_template('main/index.html',
                           title='Главная',
                           today=today,
                           max_day=max_day,
                           )


@main.route("/about")
def about():
    return render_template("main/about.html", title="О нас")


@main.route("/help")
def help():
    return render_template("main/help.html", title="Справка")
