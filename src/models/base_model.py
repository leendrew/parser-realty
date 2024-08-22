from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from src.config import config

class BaseModel(DeclarativeBase):
  __abstract__ = True

  metadata = MetaData(
    naming_convention=config.db.naming_convention,
  )
