from contextlib import contextmanager
from typing import Generator

from requests import Session as RequestsSession

from src.config import fs_config
from src.services import FileService


@contextmanager
def get_request_session() -> Generator[RequestsSession, None, None]:
    """Зависимость для получения сессии базы данных."""

    with RequestsSession() as session:
        yield session


@contextmanager
def get_fs() -> Generator[FileService, None, None]:
    """Зависимость для получения сессии базы данных в файловом сервисе."""
    with get_request_session() as r_session:
        file_service = FileService(
            session=r_session,
            host=fs_config.host,
            port=fs_config.port,
            retries=fs_config.retries,
            retry_delay_sec=fs_config.retry_delay_sec,
        )
        yield file_service
