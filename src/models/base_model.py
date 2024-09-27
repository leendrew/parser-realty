from datetime import datetime
from sqlalchemy import (
  MetaData,
  DateTime,
  func,
)
from sqlalchemy.orm import (
  DeclarativeBase,
  Mapped,
  mapped_column,
)
from src.config import config

class CreatedAtMixin:
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
  )

class UpdatedAtMixin:
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now(),
  )

class BaseModel(DeclarativeBase, CreatedAtMixin, UpdatedAtMixin):
  __abstract__ = True

  metadata = MetaData(
    naming_convention=config.db.naming_convention,
  )
