from .fastapi import FastAPIConfig
from .fs import FsConfig
from .logging import init_logging
from .pg import PgConfig
from .rabbit import RabbitConfig
from .settings import settings

app_config = FastAPIConfig(
    log_level=settings.app_log_level,
    reload=settings.app_reload,
    project_name=settings.app_name,
    app_version=settings.app_version,
)

# Настройки базы данных PostgreSQL
pg_config = PgConfig(
    host=settings.database_host,
    port=settings.database_port,
    debug_mode=settings.database_debug_mode,
    database_name=settings.database_name,
    user=settings.database_user,
    password=settings.database_password,
    connection_method=settings.database_connection_method,
    provider=settings.database_provider,
    retries=settings.database_retries,
    retry_delay_sec=settings.database_retry_delay,
)

fs_config = FsConfig(
    host=settings.file_storage_host,
    port=settings.file_storage_port,
    retries=settings.file_storage_retries,
    retry_delay_sec=settings.file_storage_retry_delay,
)

rabbit_consumer_config = RabbitConfig(
    host=settings.rabbit_host,
    port=settings.rabbit_port,
    user=settings.rabbit_worker_username,
    password=settings.rabbit_worker_password,
    vhost=settings.rabbit_worker_vhost,
    queue=settings.rabbit_queue,
    is_produser=False,
    is_consumer=True,
)

rabbit_producer_config = RabbitConfig(
    host=settings.rabbit_host,
    port=settings.rabbit_port,
    user=settings.rabbit_manager_username,
    password=settings.rabbit_manager_password,
    vhost=settings.rabbit_manager_vhost,
    queue=settings.rabbit_queue,
    is_produser=True,
    is_consumer=False,
)

__all__ = [
    "PgConfig",
    "FsConfig",
    "FastAPIConfig",
    "RabbitConfig",
    "pg_config",
    "fs_config",
    "app_config",
    "rabbit_consumer_config",
    "rabbit_producer_config",
    "init_logging",
]
