from boilerplate.db import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import bcrypt
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uuid = db.Column(db.String(32), default=uuid.uuid4().hex, nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def __init__(self, email, first_name, last_name, password):
        self.active = True
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = hash_password(password)

    def is_authenticated(self):
        return self.active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uuid

    def validate_password(self, input_password):
        return check_password(input_password, self.password)


def get_by_uuid(user_uuid):
    return User.query.filter_by(uuid=user_uuid).first()

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
