import logging
from contextlib import contextmanager
from functools import lru_cache
from typing import Generator

import sqlalchemy_utils as sa_utils
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.config import pg_config
from src.models import Base
from src.utils import retry_on_exception

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def create_engine():
    """Создает и кэширует синхронный движок базы данных."""
    logger.debug("Creating database engine")

    config = pg_config

    sync_db_url = config.database_url.replace("asyncpg", "psycopg2")

    if not sa_utils.database_exists(sync_db_url):
        sa_utils.create_database(sync_db_url)

    return sa_create_engine(config.database_url, echo=config.debug_mode)


@lru_cache(maxsize=1)
def create_database() -> sessionmaker[Session]:
    """Создает и кэширует фабрику синхронных сессий."""

    logger.debug("Creating database session factory")
    engine = create_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)


def initialize_database() -> None:
    """Создает таблицы в базе данных при старте приложения"""

    config = pg_config
    engine = create_engine()

    @retry_on_exception(
        exceptions=(SQLAlchemyError,),
        retries=pg_config.retries,
        delay_sec=config.retry_delay_sec,
    )
    def create_tables():
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")

    create_tables()


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
    except Exception:
        logger.error("Database operation failed, rolling back session")
        session.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        session.close()
