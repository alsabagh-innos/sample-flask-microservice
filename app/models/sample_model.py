import uuid as uuid

from app.models.base_model import Base
from app.singletons import db, flask_app


class SampleModel(Base):
    __tablename__ = "sample_model"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(255), nullable=False, unique=True, default=uuid.uuid4, index=True
    )
    name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __json__(self):
        return [
            "uuid",
            "name",
            "function_value",
        ]

    def __init__(self, name):
        self.name = name

    def function_value(self):
        return None


with flask_app.app_context():
    db.create_all()
