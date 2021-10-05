from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Email
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[
                           DataRequired(), Length(min=2, max=20)])
    # TODO валидация почты
    email = StringField("Почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[
                             DataRequired()])
    confirm_password = PasswordField("Подтвердите пароль", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Создать аккаунт")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Пользователь с таким именем уже существует!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Пользователь с такой почтой уже существует!")


class LoginForm(FlaskForm):
    username = StringField(
        "Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SendResetPasswordForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired(), Email()])
    submit = SubmitField("Отправить письмо")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("Новый пароль", validators=[DataRequired()])
    submit = SubmitField("Обновить пароль")
