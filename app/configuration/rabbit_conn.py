import pika
from pika.adapters.blocking_connection import BlockingConnection

from config import settings

REQUESTS_QUEUE_NAME = 'requests'

def init_rabbit() -> BlockingConnection:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(
                username=settings.RABBIT_MQ_USER,
                password=settings.RABBIT_MQ_PASSWORD
            ),
            heartbeat=0,
            blocked_connection_timeout=2
        )
    )
    return connection
