from app import db


class FlaskException(db.Model):
    __tablename__ = "flask_exception"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String())
    error = db.Column(db.String())