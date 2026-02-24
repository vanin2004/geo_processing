import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

# from fastapi.openapi.utils import get_openapi
from src.config import fastapi_config, settings
from src.injectors import initialize_database
from src.routers.api import router
from src.routers.handlers import (
    global_exception_handler,
    resource_already_exists_handler,
    resource_not_found_handler,
)

# from src.services import AlgorithmAbstractFactory
from src.services import FileAlreadyExistsError, TaskNotFoundError
from src.services import FileNotFoundError as StorageFileNotFoundError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация БД при старте; освобождение ресурсов при остановке."""
    initialize_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)
app.add_exception_handler(TaskNotFoundError, resource_not_found_handler)
app.add_exception_handler(StorageFileNotFoundError, resource_not_found_handler)
app.add_exception_handler(FileAlreadyExistsError, resource_already_exists_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    logger.info(
        f"Starting {settings.app_name} v{settings.app_version} on {fastapi_config.host}:{fastapi_config.port}"
    )

    uvicorn.run(
        "src.app:app",
        host=fastapi_config.host,
        port=fastapi_config.port if fastapi_config.port else 8000,
        log_level=fastapi_config.log_level,
        reload=fastapi_config.reload,
    )
