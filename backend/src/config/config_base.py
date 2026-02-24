from dataclasses import dataclass


@dataclass
class ConfigBase:
    """Базовый класс для конфигурации приложения."""

    pass


@dataclass
class ipConfig(ConfigBase):
    """Конфигурация для IP-адресов и портов."""

    host: str = "localhost"
    port: int | None = None


@dataclass
class RetryConfig(ConfigBase):
    """Конфигурация для параметров повторных попыток."""

    retries: int = 10
    retry_delay_sec: int = 1


@dataclass
class CreditnailsConfig(ConfigBase):
    """Конфигурация для параметров авторизации."""

    user: str = "user"
    password: str = "password"
