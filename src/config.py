from pydantic import (
  BaseModel,
  PostgresDsn,
)
from pydantic_settings import (
  BaseSettings,
  SettingsConfigDict,
)

class AppConfig(BaseModel):
  env: str = 'development'
  host: str = '0.0.0.0'
  port: int = 8080
  workers: int = 4

class DbConfig(BaseModel):
  url: PostgresDsn
  echo: bool = False
  echo_pool: bool = False
  pool_size: int = 50
  max_overflow: int = 10

  naming_convention: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
  }

class Config(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=False,
    env_nested_delimiter="_",
    env_prefix="",
    extra="allow",
  )
  app: AppConfig = AppConfig()
  db: DbConfig

config = Config()
