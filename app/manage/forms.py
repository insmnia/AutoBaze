from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User


class AddManagerForm(FlaskForm):
    username = StringField(label="Имя пользователя",
                           validators=[DataRequired()])
    submit = SubmitField("Добавить")


class AddStopForm(FlaskForm):
    name = StringField(label="Название остановки",
                       validators=[DataRequired()])
    submit = SubmitField("Добавить")
