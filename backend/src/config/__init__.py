from .fastapi import FastAPIConfig
from .fs import FsConfig
from .pg import PgConfig
from .rabbit import RabbitConfig
from .settings import settings

pg_config = PgConfig(
    database_url=settings.database_url,
    retries=settings.db_retries,
    retry_delay_sec=settings.db_retry_delay,
    debug_mode=settings.debug,
)
fs_config = FsConfig(
    host=settings.file_storage_host,
    port=settings.file_storage_port,
    timeout_seconds=settings.file_storage_timeout,
)
fastapi_config = FastAPIConfig(
    host=settings.app_host,
    port=settings.app_port,
    log_level="debug" if settings.debug else "info",
    reload=settings.debug,
)
rabbit_config = RabbitConfig(
    host=settings.rabbit_host,
    port=settings.rabbit_port,
    username=settings.rabbit_username,
    password=settings.rabbit_password,
    vhost=settings.rabbit_vhost,
    queue=settings.rabbit_queue,
)
__all__ = [
    "PgConfig",
    "FsConfig",
    "FastAPIConfig",
    "RabbitConfig",
    "pg_config",
    "fs_config",
    "fastapi_config",
    "rabbit_config",
]
