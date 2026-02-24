from contextlib import contextmanager
from typing import Generator

from src.services import WorkerService

from ..connections import get_db, get_fs


@contextmanager
def get_worker_service() -> Generator[WorkerService, None, None]:
    """Зависимость для получения WorkerService, привязанного к текущей сессии БД и FileService."""
    with get_db() as db, get_fs() as file_service:
        worker_service = WorkerService(db=db, file_service=file_service)
        yield worker_service
