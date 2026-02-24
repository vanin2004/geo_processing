import logging
import time
from contextlib import contextmanager
from functools import lru_cache
from typing import Generator

from requests import Session as RequestsSession
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.config import fs_config, pg_config, rabbit_config
from src.models import Base
from src.services import FileService, RabbitMQClient

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Базовый класс для ошибок бд"""


class DatabaseConnectionError(DatabaseError):
    """Ошибка подключения к базе данных"""


class DatabaseOperationError(DatabaseError):
    """Ошибка выполнения операции с базой данных"""


@lru_cache(maxsize=1)
def create_engine():
    """Создает и кэширует синхронный движок базы данных."""
    logger.debug("Creating database engine")

    config = pg_config
    return sa_create_engine(config.database_url, echo=config.debug_mode)


@lru_cache(maxsize=1)
def create_database() -> sessionmaker[Session]:
    """Создает и кэширует фабрику синхронных сессий."""

    logger.debug("Creating database session factory")
    engine = create_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)


def initialize_database() -> None:
    """Создает таблицы в базе данных при старте приложения (синхронно)."""

    config = pg_config
    engine = create_engine()
    retries = config.retries
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully.")
            return
        except SQLAlchemyError as e:
            if attempt < retries - 1:
                logger.warning(
                    f"Database connection failed (attempt {attempt + 1}/{retries})"
                )
                time.sleep(config.retry_delay_sec)
            else:
                raise DatabaseConnectionError(
                    f"Error creating database after {retries} attempts: {e}"
                )


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Генератор сессий базы данных для использования в FastAPI зависимостях.
    Обеспечивает автоматический commit при успехе и rollback при ошибке.
    """

    session_factory: sessionmaker[Session] = create_database()
    session: Session = session_factory()
    try:
        logger.debug("Opening new database session")
        yield session
        logger.debug("Committing database session")
        session.commit()
    except SQLAlchemyError:
        logger.error("Database operation failed, rolling back session")
        session.rollback()
        raise DatabaseOperationError("Database transaction failed and was rolled back.")
    except Exception:
        logger.error("Database operation failed, rolling back session")
        session.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        session.close()


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
            timeout_seconds=fs_config.timeout_seconds,
        )
        yield file_service


@contextmanager
def get_rabbit() -> Generator[RabbitMQClient, None, None]:
    """Зависимость для получения подключения к RabbitMQ."""

    client = RabbitMQClient(
        host=rabbit_config.host,
        port=rabbit_config.port,
        username=rabbit_config.username,
        password=rabbit_config.password,
        vhost=rabbit_config.vhost,
        queue=rabbit_config.queue,
        heartbeat=rabbit_config.heartbeat,
        blocked_connection_timeout=rabbit_config.blocked_connection_timeout,
        exchange=rabbit_config.exchange,
    )
    try:
        client.connect()
        yield client
    finally:
        client.close()
