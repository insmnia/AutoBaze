from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_app.models import User


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Мастер-пароль", validators=[DataRequired()])
    new_password = PasswordField("Новый пароль", validators=[DataRequired()])
    submit = SubmitField("Сменить")


class ChangeEmailForm(FlaskForm):
    master_password = PasswordField(
        "Мастер-пароль", validators=[DataRequired()])
    new_email = StringField("Новая почта", validators=[
                            DataRequired(), Email()])
    submit = SubmitField("Сменить")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Пользователь с такой почтой уже существует!")
