from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email
from app.models import User
import re
import string


class RegistrationForm(FlaskForm):

    username = StringField("Имя пользователя", validators=[
                           DataRequired(message="Это поле обязательно для заполнения"), Length(min=2, max=20, message="Имя должно быть от 2-х до 20-ти символов")], id="username")
    email = StringField("Почта", validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(
        granular_message=True, check_deliverability=True, message="Проверьте формат почты")])
    password = PasswordField("Пароль", validators=[
                             DataRequired(message="Это поле обязательно для заполнения"), Length(min=8, max=20, message="Длина пароля должна быть от 8-ми до 20-ти символов")])
    confirm_password = PasswordField("Подтвердите пароль", validators=[
                                     DataRequired(message="Это поле обязательно для заполнения"), EqualTo("password", message="Пароли должны совпадать")])
    submit = SubmitField("Создать аккаунт")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Пользователь с таким именем уже существует!")
        allowed = string.ascii_letters + string.digits
        for symb in username.data:
            if symb not in allowed:
                raise ValidationError(
                    "Имя пользователя может состоять только из букв и цифр")

    def validate_password(self, password):
        allowed = string.ascii_letters + string.digits+"!@#$%^&*()"
        for symb in password.data:
            if symb not in allowed:
                raise ValidationError(
                    "Пароль может состоять из цифр, букв и специальных символов( !@#$%^&*() )"
                )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Пользователь с такой почтой уже существует!")
    #     if not re.match(r"([\w\._]+@[a-z]+\.[com|ru|by]+)", email.data):
    #         raise ValidationError(
    #             "Неккоретный формат почты. Допустимые домены - com,ru,by")


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired(message="Это поле обязательно для заполнения"), Length(min=2, max=20, message="Имя может быть от 2 до 20 символов")])
    password = PasswordField("Пароль", validators=[DataRequired(
        message="Это поле обязательно для заполнения"), Length(min=8, max=20, message="Беляй отлетел")])
    submit = SubmitField("Войти")


class SendResetPasswordForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(
        granular_message=True, check_deliverability=True, message="Проверьте введенные данные"), Length(max=255, message="Беляй отлетел")])
    submit = SubmitField("Отправить письмо")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("Новый пароль", validators=[
                                 DataRequired(message="Это поле обязательно для заполнения"), Length(min=8, max=20, message="Длина пароля должна быть от 8-ми до 20-ти символов")])
    submit = SubmitField("Обновить пароль")
