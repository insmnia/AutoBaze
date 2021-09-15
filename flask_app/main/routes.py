import datetime
from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from flask_app import db
from flask_app.models import Order, Day
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    if request.method == "POST":
        date = request.form.get("calendar").split('-')
        date = datetime.date(*map(int, date))
        day = Day.query.filter_by(date=date).first()

        if day is None:
            day = Day(
                date=date, orders_amount=current_app.config['ORDERS_AMOUNT'])
            db.session.add(day)
        if request.form.get("ta") == "1":
            if day.orders_amount - int(request.form.get("amount")) < 0:
                flash("На этот день нет столько мест!")
                return redirect(url_for('main.index'))
            else:
                day.orders_amount -= int(request.form.get("amount"))
        else:
            if day.orders_amount < 20:
                flash("Невозможно выполнить грузоперевозку в этот день!")
                return redirect(url_for('main.index'))
            else:
                day.orders_amount -= 20

        order = Order(
            FCs=request.form.get("FCS"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            departure_point=request.form.get("from"),
            arrival_point=request.form.get("to"),
            order_type=request.form.get("ta"),
            amount=request.form.get("amount"),
            state="В обработке",
            creator=current_user.id,
            date=date
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
