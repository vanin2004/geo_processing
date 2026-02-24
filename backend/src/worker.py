import logging

from src.injectors.connections import get_rabbit, initialize_database
from src.injectors.services import get_worker_service

logger = logging.getLogger(__name__)


def process_task(body):
    """Функция для обработки одной задачи из очереди RabbitMQ. Вызывается при получении сообщения."""
    with get_worker_service() as worker_service:
        logger.info(f"Received task: {body}")
        worker_service.run(body)


def start_worker():
    """Функция для запуска воркера, которая инициализирует все необходимые зависимости и начинает прослушивание очереди RabbitMQ."""
    logger.debug("Initializing worker dependencies")
    initialize_database()

    with get_rabbit() as rabbit_client:
        logger.info("Worker started, waiting for tasks...")
        rabbit_client.consume(process_task)


logger.info("Worker initialization")

if __name__ == "__main__":
    start_worker()
