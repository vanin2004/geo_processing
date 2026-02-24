from contextlib import contextmanager
from typing import Generator

from src.services import TaskService

from ..connections import get_db, get_rabbit_producer


@contextmanager
def get_task_service() -> Generator[TaskService, None, None]:
    """Зависимость для получения TaskService, привязанного к текущей сессии БД."""

    with get_db() as db, get_rabbit_producer() as rabbit_client:
        task_service = TaskService(db_session=db, rabbit_client=rabbit_client)
        yield task_service
