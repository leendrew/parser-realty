from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  ForeignKey,
  UUID as PSQL_UUID,
  Integer,
  BigInteger,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from .parsing_result_model import ParsingResultModel

class UserSearchLinkModel(BaseModel):
  __tablename__ = "users_search_links"

  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  user_id: Mapped[UUID] = mapped_column(
    PSQL_UUID,
    ForeignKey(
      "users.id",
      ondelete="CASCADE",
    ),
  )

  search_link_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey(
      "search_links.id",
      ondelete="CASCADE",
    ),
    index=True,
    unique=True,
  )

  # o2m
  parsing_results: Mapped[list["ParsingResultModel"]] = relationship(
    back_populates="user_search_link",
    cascade="all, delete-orphan",
  )
