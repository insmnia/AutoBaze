from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email
from flask_app.models import User


class AddManagerForm(FlaskForm):
    username = StringField(label="Имя пользователя",
                           validators=[DataRequired()])
    submit = SubmitField("Добавить")
