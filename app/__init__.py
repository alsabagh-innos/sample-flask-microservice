from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_jwt_extended import JWTManager
import os
import app.singletons
from pymongo import MongoClient


def make_celery(app):
    # Initialize a Celery object
    celery_instance = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
        include=app.config["INCLUDE"],
        config_source="app.celeryconfig",
    )
    celery_instance.conf.update(app.config)
    celery_instance.autodiscover_tasks(app.config["INCLUDE"])

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask

    return celery_instance


def create_app():
    return flask_app


flask_app = Flask(__name__)
flask_app.config.from_pyfile("instance/config.py")

db = SQLAlchemy()
db.init_app(flask_app)

celery = make_celery(flask_app)

jwt = JWTManager(flask_app)

app.singletons.celery = celery
app.singletons.db = db
app.singletons.flask_app = flask_app
app.singletons.mongo_client = MongoClient(flask_app.config["MONGO_URI"])

from app.models import sample_model

from app.http.routes.sample_routes import sample_app

flask_app.register_blueprint(sample_app)

if os.environ.get("CRON_DEPLOYMENT") == "TRUE":
    from app.commands.sample_command import start_command_process

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=start_command_process, trigger="interval", seconds=20, max_instances=1
    )
    scheduler.start()


@flask_app.errorhandler(Exception)
def handle_custom_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 500
    return response
