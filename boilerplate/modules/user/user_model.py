from boilerplate.db import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, first_name, last_name, password):
        self.is_active = True
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = hash_password(password)
        self.creation_time = datetime.now()


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password, hashed_password):
    is_valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password)
    return is_valid_password

# Generates a default user granting access to the app should there be no users in the database
def seed_user_if_required():
    all_users = db.session.query(User).all()
    if len(all_users) == 0:
        try:
            db.session.add(User("default@default.com", "default", "user", "iloveflask!"))
            db.session.commit()
        except IntegrityError:
            # Thar be threading afoot. Ignoring integrity errors here, other threads already having created the user.
            return
