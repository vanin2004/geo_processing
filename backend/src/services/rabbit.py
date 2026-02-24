import json
import logging
import time

import pika

logger = logging.getLogger(__name__)


def retry(retries: int = 5, delay_sec: int = 1):
    """Декоратор для повторного выполнения функции при возникновении исключения."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < retries - 1:
                        logger.warning(f"Error, Retrying in {delay_sec} seconds...")
                        time.sleep(delay_sec)
                    else:
                        raise

        return wrapper

    return decorator


class RabbitMQClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        vhost: str,
        queue: str,
        heartbeat: int = 60,
        blocked_connection_timeout: int = 30,
        exchange: str = "",
    ):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._vhost = vhost
        self._queue = queue
        self._heartbeat = heartbeat
        self._blocked_connection_timeout = blocked_connection_timeout
        self._connection = None
        self._channel = None
        self._exchange = exchange

    @retry(retries=5, delay_sec=5)
    def connect(self):
        credentials = pika.PlainCredentials(self._username, self._password)
        parameters = pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            virtual_host=self._vhost,
            credentials=credentials,
            heartbeat=self._heartbeat,
            blocked_connection_timeout=self._blocked_connection_timeout,
        )
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

    def _consume_decorator(self, callback):
        logger.debug("Callback registered for RabbitMQ consumer")

        def wrapper(ch, method, properties, body: bytes):
            try:
                logger.debug(f"Received message from RabbitMQ: {body}")
                callback(body.decode("utf-8"))
            except Exception:
                logger.exception("Error processing message from RabbitMQ")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            else:
                logger.debug("Message processed successfully, acknowledging")
                ch.basic_ack(delivery_tag=method.delivery_tag)

        return wrapper

    def consume(self, callback):
        if not self._channel:
            raise RuntimeError("RabbitMQ connection is not established")
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._consume_decorator(callback),
            auto_ack=False,
        )
        try:
            logger.info(f"Started consuming from RabbitMQ queue '{self._queue}'")
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self.close()

    def publish(self, message: dict | str):
        if not self._channel:
            raise RuntimeError("RabbitMQ connection is not established")
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._queue,
            body=json.dumps(message) if isinstance(message, dict) else message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self):
        if self._connection and not self._connection.is_closed:
            self._connection.close()
