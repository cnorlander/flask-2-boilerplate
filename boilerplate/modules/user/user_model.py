from boilerplate.db import db
from boilerplate.modules.role.role_model import Role, get_role_by_name
from boilerplate.modules.role.role_actions import action_exists
from boilerplate.utils.email import send_password_reset_email
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql import func
from flask import url_for
import boilerplate.config as config
import bcrypt
import base64
import uuid
from dataclasses import dataclass


# ==============================================================================================================================================================
#                                                      User Model Class & Class Methods Definition
# ==============================================================================================================================================================
# Using Python Dataclasses. Haven't seen this with many Flask examples but it works well for automatic JSON conversion:
# https://docs.python.org/3/library/dataclasses.html
@dataclass
class User(db.Model):
    id: int
    uuid: str
    active: bool
    first_name: str
    last_name: str
    email: str
    creation_time: datetime

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    uuid = db.Column(db.Uuid, index=True, nullable=False, unique=True, default=uuid.uuid4)
    active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.fromtimestamp(0), nullable=False)
    creation_time = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    reset_code = db.Column(db.String(32), default="NORESET", nullable=False, unique=False)
    reset_time = db.Column(db.DateTime, default=datetime.fromtimestamp(0), nullable=False)
    role_uuid = db.Column(db.Uuid, db.ForeignKey('role.uuid'), nullable=False)
    role = db.relationship("Role", back_populates="users")

    def __init__(self, email: str, first_name: str, last_name: str, password: str, role: Role):
        self.active = True
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = hash_password(password)
        self.role = role

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uuid

    def validate_password(self, input_password: str):
        return check_password(input_password, self.password)

    def validate_reset_code(self, reset_code: str):
        if self.reset_code == "NORESET":
            return False
        difference = datetime.utcnow() - self.reset_time
        if (difference.seconds < config.PASSWORD_RESET_CODE_VALIDITY * 60) and self.reset_code == reset_code:
            return True
        return False

    def has_reset_code(self):
        difference = datetime.utcnow() - self.reset_time
        if (difference.seconds < config.PASSWORD_RESET_CODE_VALIDITY * 60):
            return True
        return False

    def get_initials(self):
        return (self.first_name[0] + self.last_name[0]).upper()

    def update_password(self, new_password: str):
        self.password = hash_password(new_password)
        self.reset_code = "NORESET"
        self.reset_time = datetime.fromtimestamp(0)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def update_last_logon(self):
        self.last_login = func.now()
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def can(self, action_name: str):
        # action_exists confirms the action is registered. If not it will toss an exception.
        action_exists(action_name)
        if action_name in self.role.actions:
            return True
        return False

# ==============================================================================================================================================================
#                                                      Anonymous User Class & Methods Definition
# ==============================================================================================================================================================
class AnonymousUser():
    @property
    def role(self):
        return get_role_by_name("Anonymous")

    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None

    def can(self, *args):
        return False

# ==============================================================================================================================================================
#                                                             Non-Class Utility Functions
# ==============================================================================================================================================================
def get_by_uuid(user_uuid):
    if isinstance(user_uuid, str):
        user_uuid = uuid.UUID(user_uuid)
    return db.session.query(User).filter_by(uuid=user_uuid).first()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password: str, hashed_password: bytes):
    is_valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password)
    return is_valid_password

def check_password_requirements(new_password: str):
    password_rules_broken = []
    if len(new_password) < config.PASSWORD_MIN_CHARACTERS:
        password_rules_broken.append(f"Password is too short. Passwords should contain at least {config.PASSWORD_MIN_CHARACTERS} characters.")
    if len(new_password) > config.PASSWORD_MAX_CHARACTERS:
        password_rules_broken.append(f"Password is too long. Passwords should contain at most {config.PASSWORD_MAX_CHARACTERS} characters.")
    if config.PASSWORD_REQUIRE_NUMERALS and (not any(char.isdigit() for char in new_password)):
        password_rules_broken.append(f"Password must contain at least one number.")
    if config.PASSWORD_REQUIRE_UPPER_CASE and (not any(char.isupper() for char in new_password)):
        password_rules_broken.append(f"Password must contain at least one upper case letter.")
    if config.PASSWORD_REQUIRE_LOWER_CASE and (not any(char.islower() for char in new_password)):
        password_rules_broken.append(f"Password must contain at least one lower case letter.")
    if config.PASSWORD_REQUIRE_SPECIAL_CHARACTERS and (not any(char in config.PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS for char in new_password)):
        password_rules_broken.append(f"Password must contain at least one special symbol.")
    return password_rules_broken

def send_password_reset(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        # Rate limit the responses prevents a bot from spamming the user with password resets
        if user.has_reset_code():
            return "rate-limit"

        # Create the URL safe unique password reset code and save it to the database
        user.reset_code = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
        user.reset_time = func.now()
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return "error"
        reset_url = f"{config.BASE_URL}{url_for('get_password_reset_screen')}?uuid={user.uuid}&reset-code={user.reset_code}"

        # TODO: You will need to find the send_password_reset_email function in boilerplate.utils.email and implement it yourself!
        send_password_reset_email(user.email, reset_url)
        print(f"Email sending not currently configured. Please see the comments in send_password_reset within email.py under utils.\n"
              f"User with email address {user.email} should be sent: {reset_url}", flush=True)
        return "success"
    return "fail"

def replace_all_instances_of_role(existing_role: Role, new_role: Role):
    try:
        users = User.query.filter_by(role_uuid=existing_role.uuid).update({'role_uuid': new_role.uuid})
        db.session.commit()
    except:
        db.session.rollback()
        raise


def create_if_not_exists(user: User):
    db_users = db.session.query(User).filter_by(email=user.email).all()
    if len(db_users) == 0:
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Thar be threading afoot. Ignoring integrity errors here, other threads already having created the user.
            return


# Generates a default user granting access to the app should there be no users in the database
def seed_user_if_required():
    if config.DB_SEED:
        all_users = db.session.query(User).all()
        admin_role = get_role_by_name("System Admin")
        default_role = get_role_by_name("Default Role")
        if len(all_users) == 0:
            create_if_not_exists(User("admin@default.com", "Admin", "User", "iloveflask!", admin_role))
            create_if_not_exists(User("default@default.com", "Default", "User", "iloveflask!", default_role))
