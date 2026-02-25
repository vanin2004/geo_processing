from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс настроек приложения.
    Все поля могут быть переопределены через переменные окружения.
    """

    # Основные настройки приложения
    app_log_level: str = "info"
    app_reload: bool = False
    app_name: str = "Image Processing API"
    app_version: str = "3.0.0"

    # Настройки базы данных PostgreSQL
    database_host: str = "localhost"
    database_port: int = 5432
    database_debug_mode: bool = False
    database_name: str = "geo_img_db"
    database_user: str = "postgres"
    database_password: str = "password"
    database_connection_method: str = "psycopg2"
    database_provider: str = "postgresql"
    database_retries: int = 10
    database_retry_delay: int = 1

    # Настройки файлового хранилища
    file_storage_host: str = "localhost"
    file_storage_port: int = 9000
    file_storage_retries: int = 30
    file_storage_retry_delay: int = 1

    # Настройки RabbitMQ
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_queue: str = "image_processing_queue"

    rabbit_worker_username: str = "guest"
    rabbit_worker_password: str = "guest"
    rabbit_worker_vhost: str = "/"

    rabbit_manager_username: str = "guest"
    rabbit_manager_password: str = "guest"
    rabbit_manager_vhost: str = "/"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
