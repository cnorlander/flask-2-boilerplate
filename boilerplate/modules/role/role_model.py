from boilerplate.db import db
from sqlalchemy.sql import func
from typing import List
import uuid
import json

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uuid = db.Column(db.String(32), default=uuid.uuid4().hex, nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    actions = db.Column(db.JSON, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def __init__(self, name:str, description: str, actions: List[dict]):
        self.active = True
        self.name = name
        self.description = description
        self.actions = json.dumps(actions)

#TODO: Write code to cleanup old removed actions.
def action_clean_up():
    pass