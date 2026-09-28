from Backend.extensions import db
from Backend.models.videos import Video

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    video = db.relationship('Video', backref='transcripts')
    start_time = db.Column(db.Float,nullable=False)
    end_time = db.Column(db.Float,nullable=False)
   