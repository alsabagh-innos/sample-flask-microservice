import os

# Broker settings (example: using Redis)
BROKER_URL = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0'
CELERY_RESULT_BACKEND = (
    f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0'
)

# Task result expiration time (in seconds)
CELERY_TASK_RESULT_EXPIRES = 3600

# Import paths for tasks
CELERY_IMPORTS = ("app.tasks",)  # Replace 'myapp.tasks' with your actual task module

# Concurrency settings
CELERYD_CONCURRENCY = 8  # Number of worker processes/threads

# Serialization format (e.g., JSON)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Additional settings (e.g., timezone)
CELERY_TIMEZONE = "UTC"

# Log settings
CELERYD_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
CELERYD_LOG_LEVEL = "INFO"
