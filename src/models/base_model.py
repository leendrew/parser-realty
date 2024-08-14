from sqlalchemy import MetaData
from sqlalchemy.orm import (
  DeclarativeBase,
  declared_attr,
)
from src.config import config
from src.utils import camel_case_to_snake_case

class BaseModel(DeclarativeBase):
  __abstract__ = True

  metadata = MetaData(
    naming_convention=config.db.naming_convention,
  )

  @declared_attr.directive
  def __tablename__(cls) -> str:
    return camel_case_to_snake_case(cls.__name__)
