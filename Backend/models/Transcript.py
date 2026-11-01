
from Backend.extensions import db
from Backend.models.videos import Video


class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Legacy database columns
    text = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.Float, nullable=False)

    # Current columns
    raw_text = db.Column(db.Text, nullable=False)
    semantic_text = db.Column(db.Text, nullable=False)

    video_id = db.Column(
        db.Integer,
        db.ForeignKey("video.id"),
        nullable=False
    )

    video = db.relationship("Video", backref="transcripts")

    start = db.Column(db.Float, nullable=True)
    end = db.Column(db.Float, nullable=True)
