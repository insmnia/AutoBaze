from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import Stop, User


class AddManagerForm(FlaskForm):
    username = StringField(label="Имя пользователя",
                           validators=[DataRequired()])
    submit = SubmitField("Добавить")

    def validate_manager(self,username):
        if User.query.filter_by(username=username.data).first().manager:
            raise ValidationError("Такой менеджер уже есть!")


class AddStopForm(FlaskForm):
    name = StringField(label="Название остановки",
                       validators=[DataRequired()])
    submit = SubmitField("Добавить")

    def validate_stop(self,name):
        if Stop.query.filter_by(name=name.data).first():
            raise ValidationError("Такая остановка уже есть!")
