from config import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(80), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=True)
    level = db.Column(db.String(80), nullable=False)
    content_duration = db.Column(db.Float, nullable=True)
    subject = db.Column(db.String(80), nullable=False)
