from Backend.extensions import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)

    #define the foreign key to the conversation table(simply get access to the conversation id)
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversation.id"),
        nullable=False
    )

    role = db.Column(db.String(20), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Connect message back to its conversation
    conversation = db.relationship(
        "Conversation",
        back_populates="messages"
    )