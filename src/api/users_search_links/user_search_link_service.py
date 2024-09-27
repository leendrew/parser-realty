from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import (
  HTTPException,
  Depends,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_search_link_model import UserSearchLinkModel
# ! MIGRATION: comment below and uncomment next before migration
from src.models.search_link_model import SearchLinkModel
# class SearchLinkModel:
#   pass

logger = Logger().get_instance()

class UserSearchLinkService(BaseService):
  async def get_all_by(
    self,
    id: int | None = None,
    user_id: UUID | None = None,
    search_link_id: int | None = None,
    is_link_active: bool | None = None,
  ) -> Sequence[UserSearchLinkModel]:
    stmt = (
      select(UserSearchLinkModel)
      .join(UserSearchLinkModel.user)
      # load to response
      # .options(joinedload(UserSearchLinkModel.user))
      .join(UserSearchLinkModel.search_link)
      # load to response
      # .options(joinedload(UserSearchLinkModel.search_link))
    )

    filters = []
    if id is not None:
      filters.append(UserSearchLinkModel.id == id)
    if user_id is not None:
      filters.append(UserSearchLinkModel.user_id == user_id)
    if search_link_id is not None:
      filters.append(UserSearchLinkModel.search_link_id == search_link_id)
    if is_link_active is not None:
      filters.append(SearchLinkModel.is_active == is_link_active)

    if filters:
      stmt = stmt.filter(*filters)

    result = await self.session.scalars(stmt)

    return result.all()

UserSearchLinkServiceDependency = Annotated[UserSearchLinkService, Depends()]