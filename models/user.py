from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = "flask_user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(5), nullable=False)