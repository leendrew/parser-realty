from enum import Enum
from pydantic import (
  BaseModel,
  PostgresDsn,
)
from pydantic_settings import (
  BaseSettings,
  SettingsConfigDict,
)

class AppEnv(Enum):
  development = "development"
  production = "production"

class AppConfig(BaseModel):
  env: AppEnv
  host: str
  port: int
  workers: int

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

class TgConfig(BaseModel):
  botapikey: str

class Config(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=False,
    env_nested_delimiter="_",
    env_prefix="",
    extra="allow",
  )
  app: AppConfig
  db: DbConfig
  tg: TgConfig

config = Config()
