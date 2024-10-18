from api import db
from sqlalchemy.sql import func


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),)
    password = db.Column(db.String(100))
    sentDate = db.Column(db.DateTime(timezone=True), default=func.now())
    Isverify = db.Column(db.Integer)
    role = db.Column(db.String(50))