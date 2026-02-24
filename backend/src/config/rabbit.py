from dataclasses import dataclass

from .config_base import CreditnailsConfig, IpConfig, RetryConfig


@dataclass
class RabbitConfig(RetryConfig, IpConfig, CreditnailsConfig):
    """Конфигурация подключения к RabbitMQ."""

    vhost: str = "/"
    queue: str = "tasks"
    heartbeat: int = 60
    blocked_connection_timeout: int = 30
    exchange: str = ""
    is_produser: bool = False
    is_consumer: bool = False
