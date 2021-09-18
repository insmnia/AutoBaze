from app import db
from app.models import User

u = User.query.filter_by(username=input("username:")).first()
if u:
    u.manager = 1
    db.session.commit()
    print("User is now admin")
else:
    print("User not found")
