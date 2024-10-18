from api import db
from sqlalchemy.sql import func


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100),)
    sentDate = db.Column(db.DateTime(timezone=True), default=func.now())