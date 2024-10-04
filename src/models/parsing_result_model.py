from typing import TYPE_CHECKING
from sqlalchemy import (
  ForeignKey,
  BigInteger,
  SmallInteger,
  Text,
)
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_search_link_model import UserSearchLinkModel

class ParsingResultModel(BaseModel):
  __tablename__ = "parsing_results"

  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  user_search_link_id: Mapped[int] = mapped_column(
    BigInteger,
    ForeignKey(
      "users_search_links.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  user_search_link: Mapped["UserSearchLinkModel"] = relationship(
    back_populates="parsing_results",
  )

  direct_link: Mapped[str] = mapped_column(
    Text,
    index=True,
  )

  price: Mapped[int] = mapped_column(
    BigInteger,
  )

  commission_percent: Mapped[int | None] = mapped_column(
    SmallInteger,
    nullable=True,
  )

  deposit_percent: Mapped[int | None] = mapped_column(
    SmallInteger,
    nullable=True,
  )
