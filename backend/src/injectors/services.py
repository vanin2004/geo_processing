from contextlib import contextmanager
from typing import Generator

from src.injectors.connections import get_db, get_fs, get_rabbit
from src.services import (
    AlgorithmAbstractFactory,
    TaskService,
    WorkerService,
)


@contextmanager
def get_task_service() -> Generator[TaskService, None, None]:
    """Зависимость для получения TaskService, привязанного к текущей сессии БД."""

    with get_db() as db, get_rabbit() as rabbit_client:
        task_service = TaskService(db_session=db, rabbit_client=rabbit_client)
        yield task_service


@contextmanager
def get_worker_service() -> Generator[WorkerService, None, None]:
    """Зависимость для получения WorkerService, привязанного к текущей сессии БД и FileService."""
    with get_db() as db, get_fs() as file_service:
        worker_service = WorkerService(db=db, file_service=file_service)
        yield worker_service


def get_algorithm_factory() -> type[AlgorithmAbstractFactory]:
    """Зависимость для получения фабрики алгоритмов."""
    return AlgorithmAbstractFactory
