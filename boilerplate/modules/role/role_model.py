from boilerplate.db import db
from boilerplate.modules.role import get_action_names
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from typing import List
import uuid
import json
from datetime import datetime
from dataclasses import dataclass

# Using Python Dataclasses. Haven't seen this with many Flask examples but it works well for automatic JSON conversion:
# https://docs.python.org/3/library/dataclasses.html
@dataclass
class Role(db.Model):
    # Dataclass definitions
    id: int
    uuid: str
    active: bool
    hidden: bool
    system: bool
    name: str
    description: str
    actions: db.JSON
    creation_time: datetime

    # Model Definitions
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uuid = db.Column(db.String(32), default=uuid.uuid4().hex, nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    hidden = db.Column(db.Boolean, default=False, nullable=False)
    system = db.Column(db.Boolean, default=False, nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    actions = db.Column(db.JSON, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    # Primary constructor
    def __init__(self, name: str, description: str, actions: List[dict], hidden: bool = False, system: bool = False, active: bool = True):
        self.active = active
        self.system = system
        self.hidden = hidden
        self.name = name
        self.description = description
        self.actions = actions

# updates system level roles to reflect all possible actions
def update_system_roles():
    rows_changed = Role.query.filter_by(system=True).update({'actions':get_action_names()})
    db.session.commit()

# Will create a role if a role with that name doesn't already exist
def create_if_not_exists(role: Role):
    db_roles = db.session.query(Role).filter_by(name=role.name).all()
    if len(db_roles) == 0:
        try:
            db.session.add(role)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Thar be threading afoot. Ignoring integrity errors here, other threads already having created the user.
            return

# Will seed the Roles table in the db with some default roles.
def seed_roles_if_required():
    create_if_not_exists(Role("System", "Global Role for the System it's self.", [], system=True, hidden=True))
    create_if_not_exists(Role("System Admin", "Global Role for a System Admin.", [], system=True, hidden=False))
    create_if_not_exists(Role("Test Role", "Global Role for a System Admin.", [get_action_names()[1]]))