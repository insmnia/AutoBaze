from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_app import bcrypt, db
from flask_app.models import Order
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    if request.method == "POST":
        order = Order(
            FCs=request.form.get("FCS"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
            departure_point=request.form.get("from"),
            arrival_point=request.form.get("to"),
            order_type=request.form.get("ta"),
            amount=request.form.get("amount"),
            state="В обработке"
        )
        db.session.add(order)
        db.session.commit()
        flash("Заявка успешно отправлена! Ожидайте обратной связи")
    return render_template('main/index.html',
                           title='Главная',
                           )
