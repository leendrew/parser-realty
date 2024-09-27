from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import (
  BigInteger,
  UUID as PSQL_UUID,
  ForeignKey,
)
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_model import UserModel

class UserTelegramModel(BaseModel):
  __tablename__ = "users_telegrams"

  telegram_id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
  )

  user_id: Mapped[UUID] = mapped_column(
    PSQL_UUID,
    ForeignKey(
      "users.id",
      ondelete="CASCADE",
    ),
  )
  # o2o
  user: Mapped["UserModel"] = relationship(
    back_populates="telegram",
  )
