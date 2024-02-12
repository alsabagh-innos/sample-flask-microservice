import os


FLASK_ENV = "development"
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_RECYCLE = 1800

# MongoDB's configuration with username and password
MONGO_URI = f'{os.environ.get("MONGO_URI")}'


# Celery configuration
CELERY_BROKER_URL = (
    f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0'
)
CELERY_RESULT_BACKEND = (
    f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0'
)
INCLUDE = ["app.tasks"]

# JWT configuration
JWT_SECRET_KEY = os.environ.get("JWT_SECRET")
JWT_DECODE_ALGORITHMS = "HS256"
