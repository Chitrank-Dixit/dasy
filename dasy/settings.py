import os

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "testdb")
DB_USER = os.environ.get("DB_USER", "testuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "db123")


DB_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

AMQP_HEARTBEAT = os.environ.get("AMQP_HEARTBEAT", 20)
AMQP_MAX_RETRIES = os.environ.get("AMQP_MAX_RETRIES", 3)

EXCHANGE = os.environ.get("EXCHANGE", "product_consumer_exchange")
SLEEP_INTERVAL_ON_PUBLISH_EXCEPTION = 5
PERSISTENT_DELIVERY_MODE = 2

RABBITMQ_URL = "amqp://{}:{}@{}:{}/".format(
    os.environ.get("RABBIT_USER", "testuser"),
    os.environ.get("RABBIT_PASSWORD", "testpass"),
    os.environ.get("RABBIT_ADDR", "127.0.0.1"),
    os.environ.get("RABBIT_PORT", "5672"),
)