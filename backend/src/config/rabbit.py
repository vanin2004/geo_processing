from dataclasses import dataclass

from .config_base import ConfigBase


@dataclass
class RabbitConfig(ConfigBase):
    """Конфигурация подключения к RabbitMQ."""

    host: str = "localhost"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"
    vhost: str = "/"
    queue: str = "tasks"
    heartbeat: int = 60
    blocked_connection_timeout: int = 30
    exchange: str = ""
