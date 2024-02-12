from app import celery, flask_app


@celery.task(bind=True, max_retries=5, default_retry_delay=10)
def sample_task(self):
    with flask_app.app_context():
        pass
