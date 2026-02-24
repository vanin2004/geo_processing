import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import app_config
from src.injectors import initialize_database
from src.routers.api import router
from src.routers.handlers import (
    global_exception_handler,
    resource_already_exists_handler,
    resource_not_found_handler,
)
from src.services import FileAlreadyExistsError, TaskNotFoundError
from src.services import FileNotFoundError as StorageFileNotFoundError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация БД при старте; освобождение ресурсов при остановке."""
    initialize_database()
    yield


app = FastAPI(
    title=app_config.project_name,
    version=app_config.app_version,
    debug=app_config.log_level == "debug",
    lifespan=lifespan,
)
app.add_exception_handler(TaskNotFoundError, resource_not_found_handler)
app.add_exception_handler(StorageFileNotFoundError, resource_not_found_handler)
app.add_exception_handler(FileAlreadyExistsError, resource_already_exists_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(router)


logger.info(f"Starting {app_config.project_name} v{app_config.app_version}")
