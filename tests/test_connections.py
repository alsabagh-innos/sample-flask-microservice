import os
import unittest
from redis import Redis
from app import create_app


class TestConnections(unittest.TestCase):
    def setUp(self):
        # Set up a Flask test client and configure it
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_redis_connection(self):
        # Check the Redis connection
        with self.app.app_context():
            redis = Redis.from_url(
                os.environ.get(
                    "CELERY_BROKER_URL",
                    f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0',
                )
            )
            self.assertTrue(redis.ping())

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
