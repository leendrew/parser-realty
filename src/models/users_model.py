from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import func
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import SearchLinksModel
  from . import UsersSearchLinksModel

class Users(BaseModel):
  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )

  # m2m
  search_links: Mapped[list["SearchLinksModel"]] = relationship(
    back_populates="users",
    secondary="users_search_links",
  )

  # o2m
  user_search_links: Mapped[list["UsersSearchLinksModel"]] = relationship(
    back_populates="user",
  )
