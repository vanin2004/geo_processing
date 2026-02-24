from dataclasses import dataclass

from .config_base import CreditnailsConfig, RetryConfig, ipConfig


@dataclass
class PgConfig(RetryConfig, ipConfig, CreditnailsConfig):
    debug_mode: bool = False
    database_name: str = "geo_img_db"
    connection_method: str = "psycopg2"
    provider: str = "postgresql"

    @property
    def database_url(self) -> str:
        return f"{self.provider}+{self.connection_method}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"
