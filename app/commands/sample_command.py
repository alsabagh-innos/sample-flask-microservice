from app.singletons import flask_app, db


def start_command_process():
    with flask_app.app_context():
        db.engine.dispose()
        print("Starting command process")
