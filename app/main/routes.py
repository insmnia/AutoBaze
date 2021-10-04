import datetime
from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Order, Day
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    if request.method == "POST":

        Fcs = request.form.get("FCS")
        phone = request.form.get("phone")
        email = request.form.get("email")
        departure_point = request.form.get("from")
        arrival_point = request.form.get("to")
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
