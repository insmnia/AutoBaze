from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_app import bcrypt, db
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', "POST"])
@login_required
def index():
    return render_template('main/index.html',
                           title='Главная',
                           )
