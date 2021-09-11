from flask_app import create_app, db
from flask_app.models import User, Password

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Password': Password}
