from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from app.config import Config
# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.sign_in'
login_manager.login_message_category = 'info'
login_manager.login_message = "Войдите, чтобы продолжить"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    from app.auth.routes import auth
    from app.main.routes import main
    from app.profile.routes import prof
    from app.manage.routes import manage
    from app.errors import errors
    app.register_blueprint(auth, prefix="/auth")
    app.register_blueprint(main)
    app.register_blueprint(manage, prefix="/manage")
    app.register_blueprint(prof, prefix="/user")
    app.register_blueprint(errors)

    @app.template_filter('date')
    def datetimeformat(value):  # 2021-09-05 00:15:40.738222
        date = str(value).split()[0].split("-")
        return f"{date[-1]} {date[-2]} {date[-3]}"

    return app
