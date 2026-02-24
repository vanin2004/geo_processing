from dataclasses import dataclass

from .config_base import ConfigBase


@dataclass
class FastAPIConfig(ConfigBase):
    log_level: str = "info"
    reload: bool = False
    project_name: str = "Image Processing API"
    app_version: str = "3.0.0"
