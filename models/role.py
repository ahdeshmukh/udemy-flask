from app import db

class Role(db.Model):
    __tablename__ = "flask_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))