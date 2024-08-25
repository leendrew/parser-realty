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
from src.shared import BaseService
from src.utils import LinkValidator
# ! MIGRATION: comment below before migration
from src.models.search_link_model import SearchLinkModel
from src.models.user_model import UserModel
from .search_link_types import SourceName

class SearchLinkService(BaseService):
  async def create_one_to_user(self,
    link: str,
    source_name: SourceName,
    user: UserModel,
  ) -> SearchLinkModel:
    is_link_https = LinkValidator.is_valid_https(link)
    if not is_link_https:
      # TODO: log uncorrect protocol
      print(f"Ссылка \"{link}\" имеет невалидный протокол")

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Невалидный протокол",
      )

    is_valid_source_link = LinkValidator.is_valid_source(source=source_name, link=link)
    if not is_valid_source_link:
      # TODO: log link not support
      print(f"Ссылки с ресурса \"{source_name}\" не поддерживаются")

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ссылки данного сайта не поддерживаются",
      )

    model = SearchLinkModel(
      search_link=link,
      source_name=source_name.value,
    )
    model.users.append(user)

    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception as e:
      # TODO: log corrupt save search link
      print(f"Ошибка при сохранении ссылки \"{link}\" в базу для пользователя с id \"{user_id}\". Ошибка: {e}")

      await self.session.rollback()

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при сохранении ссылки",
      )

  async def get_all_by(
    self,
    id: int | None,
    source_name: SourceName | None,
    user_id: UUID | None,
  ) -> Sequence[SearchLinkModel]:
    stmt = select(SearchLinkModel).join(SearchLinkModel.users)

    filters = []

    if id is not None:
      filters.append(SearchLinkModel.id == id)
    if source_name is not None:
      filters.append(SearchLinkModel.source_name == source_name.value)
    if user_id is not None:
      filters(UserModel.id == user_id)

    if filters:
      stmt = stmt.filter(*filters)

    links = await self.session.scalars(stmt)

    return links.all()

SearchLinkServiceDependency = Annotated[SearchLinkService, Depends()]
