import datetime
from flask import render_template, request, Blueprint, flash
from flask_login import login_required, current_user
from flask_app import db
from flask_app.models import Order
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    if request.method == "POST":
        date = request.form.get("calendar").split('-')
        date = datetime.date(*map(int, date))
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
