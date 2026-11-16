from Backend.extensions import db
from datetime import datetime, timezone


class Conversation(db.Model):
    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    title = db.Column(db.String(120), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # One conversation can contain many messages
    messages = db.relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at"
    )

    # Connect conversation back to its owner
    user = db.relationship(
        "User",
        back_populates="conversations"
    )
    # it tells the conversation is belong to which video 
    video_id = db.Column(
    db.Integer,
    db.ForeignKey("video.id"),
    nullable=False
    )


    # we difine the rule that one user can only have one conversation per video
    __table__args__ = (
        db.UniqueConstraint(
            "user_id",
            "video_id",
            name="unique_user_video_conversation"
        )
    )

    user = db.relationship(
    "User",
    back_populates="conversations"
    )

