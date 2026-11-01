from sqlalchemy import inspect
from Backend.app import app
from Backend.extensions import db

with app.app_context():
    print("Database URL:", db.engine.url)
    print(
        "Transcript columns:",
        [c["name"] for c in inspect(db.engine).get_columns("transcript")]
    )