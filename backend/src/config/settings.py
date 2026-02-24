from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс настроек приложения.
    Все поля могут быть переопределены через переменные окружения.
    """

    # Основные настройки приложения
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_name: str = "Image Processing API"
    app_version: str = "3.0.0"
    debug: bool = False

    # Настройки файлового хранилища
    file_storage_host: str = "http://localhost"
    file_storage_port: int = 9000
    file_storage_timeout: int = 30

    # Настройки подключения к БД
    database_url: str = "postgresql+psycopg2://postgres:postgres@db/img_processing"
    db_retries: int = 5
    db_retry_delay: int = 2

    # Настройки подключения к RabbitMQ
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_username: str = "guest"
    rabbit_password: str = "guest"
    rabbit_vhost: str = "/"
    rabbit_queue: str = "tasks"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
