from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.models import User
import re


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Старый пароль", validators=[DataRequired(message="Это поле обязательно для заполнения"), Length(min=8, max=20, message="Длина пароля должна быть от 8-ми до 20-ти символов")])
    new_password = PasswordField("Новый пароль", validators=[
                                 DataRequired(message="Это поле обязательно для заполнения")])
    submit = SubmitField("Сменить")


class ChangeEmailForm(FlaskForm):
    master_password = PasswordField(
        "Пароль", validators=[DataRequired(message="Это поле обязательно для заполнения")])
    new_email = StringField("Новая почта", validators=[
                            DataRequired(message="Это поле обязательно для заполнения"), Email(
                                granular_message=True, check_deliverability=True, message="Проверьте введенные данные")])
    submit = SubmitField("Сменить")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Пользователь с такой почтой уже существует!")
        # if not re.match(r"([\w\._]+@[a-z]+\.[com|ru|by]+)", email.data):
        #     raise ValidationError(
        #         "Неккоретный формат почты. Допустимые домены - com,ru,by")
