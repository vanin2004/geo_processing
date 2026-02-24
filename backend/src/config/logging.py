import logging
import sys

from src.config.settings import settings

_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
)
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def init_logging():
    match settings.app_log_level.lower():
        case "debug":
            level = logging.DEBUG
        case "info":
            level = logging.INFO
        case "warning":
            level = logging.WARNING
        case "error":
            level = logging.ERROR
        case _:
            level = logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
