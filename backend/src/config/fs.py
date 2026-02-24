from dataclasses import dataclass

from .config_base import IpConfig, RetryConfig


@dataclass
class FsConfig(IpConfig, RetryConfig):
    pass
