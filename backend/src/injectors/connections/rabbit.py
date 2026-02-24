from contextlib import contextmanager
from typing import Generator

from src.config import rabbit_consumer_config, rabbit_producer_config
from src.services import RabbitMQClient


@contextmanager
def get_rabbit_consumer() -> Generator[RabbitMQClient, None, None]:
    """Зависимость для получения подключения к RabbitMQ."""

    client = RabbitMQClient(
        host=rabbit_consumer_config.host,
        port=rabbit_consumer_config.port,
        username=rabbit_consumer_config.user,
        password=rabbit_consumer_config.password,
        vhost=rabbit_consumer_config.vhost,
        queue=rabbit_consumer_config.queue,
        heartbeat=rabbit_consumer_config.heartbeat,
        blocked_connection_timeout=rabbit_consumer_config.blocked_connection_timeout,
        exchange=rabbit_consumer_config.exchange,
    )
    try:
        client.connect()
        yield client
    finally:
        client.close()


@contextmanager
def get_rabbit_producer() -> Generator[RabbitMQClient, None, None]:
    """Зависимость для получения подключения к RabbitMQ."""

    client = RabbitMQClient(
        host=rabbit_producer_config.host,
        port=rabbit_producer_config.port,
        username=rabbit_producer_config.user,
        password=rabbit_producer_config.password,
        vhost=rabbit_producer_config.vhost,
        queue=rabbit_producer_config.queue,
        heartbeat=rabbit_producer_config.heartbeat,
        blocked_connection_timeout=rabbit_producer_config.blocked_connection_timeout,
        exchange=rabbit_producer_config.exchange,
    )
    try:
        client.connect()
        yield client
    finally:
        client.close()
