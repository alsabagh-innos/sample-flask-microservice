from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.collections import InstrumentedList
import enum


from app.singletons import db, flask_app


class Base(db.Model):
    __abstract__ = True

    def to_json(self):
        json_data = {}
        if hasattr(self, "__json__"):
            attributes = self.__json__()
        else:
            # If __json__ is not defined, use all attributes
            attributes = self.__dict__.keys()

        for attr in attributes:
            if attr.startswith("_"):
                # Skip private and protected attributes
                continue

            try:
                value = getattr(self, attr)

                if isinstance(value, enum.Enum):
                    # Convert Enum to its name
                    json_data[attr] = value.name
                elif isinstance(value, Base):
                    # Serialize related SQLAlchemy Base instances
                    json_data[attr] = value.to_json()
                elif isinstance(value, InstrumentedList):
                    # Serialize each item in the InstrumentedList
                    json_data[attr] = [item.to_json() for item in value]
                elif isinstance(value, list):
                    # Serialize each item in the InstrumentedList
                    json_data[attr] = [item.to_json() for item in value]
                else:
                    if callable(value):
                        json_data[attr] = value()
                    else:
                        json_data[attr] = value
            except AttributeError:
                # Skip attributes that are not defined on the model
                pass

        return json_data

    def save(self):
        """Save the current instance to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e  # You may want to handle or log this exception

    def update(self, **kwargs):
        """Update attributes of the current instance and save it to the database."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self):
        """Delete the current instance from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


with flask_app.app_context():
    db.create_all()
