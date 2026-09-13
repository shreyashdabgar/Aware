from Backend.extensions import db
from Backend.models.videos import Video
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    videos = db.relationship('Video', backref='owner', lazy=True)
