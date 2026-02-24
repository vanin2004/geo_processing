import logging
import time

logger = logging.getLogger(__name__)


def retry(retries: int = 5, delay_sec: int = 1):
    """Декоратор для повторного выполнения функции при возникновении исключения."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < retries - 1:
                        logger.warning(
                            f"Error occurred, retrying in {delay_sec} seconds... (Attempt {attempt + 1}/{retries})"
                        )
                        time.sleep(delay_sec)
                    else:
                        raise

        return wrapper

    return decorator
