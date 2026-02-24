from dataclasses import dataclass

from .config_base import RetryConfig, ipConfig


@dataclass
class FsConfig(ipConfig, RetryConfig):
    pass
