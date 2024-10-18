from api import db
from sqlalchemy.sql import func


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),)
    OTPcode = db.Column(db.String(100))
    sentDate = db.Column(db.DateTime(timezone=True), default=func.now())
    Isverify = db.Column(db.Integer)
    
class TOKEN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tokenid = db.Column(db.String(100),)

