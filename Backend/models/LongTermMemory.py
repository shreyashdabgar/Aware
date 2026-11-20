from Backend.extensions import db
from datetime import datetime,timezone

class LongTermMemory(db.Model):
    __tablename__ = "long_term_memory"

    #fields i want in the table
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    fact = db.Column(db.String, nullable = False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
