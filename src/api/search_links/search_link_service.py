from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import (
  HTTPException,
  Depends,
)
from sqlalchemy import (
  select,
  update,
  delete,
)
from src.shared import (
  BaseService,
  Logger,
)
from src.utils import LinkValidator
# ! MIGRATION: comment below before migration
from src.models.search_link_model import SearchLinkModel
from src.models.user_model import UserModel
from .search_link_types import SourceName

logger = Logger().get_instance()

class SearchLinkService(BaseService):
  async def create_one_to_user(
    self,
    link: str,
    source_name: SourceName,
    user: UserModel,
  ) -> SearchLinkModel:
    is_link_https = LinkValidator.is_valid_https(link)
    if not is_link_https:
      logger.error(f"Ссылка \"{link}\" имеет невалидный протокол")

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Невалидный протокол",
      )

    is_valid_source_link = LinkValidator.is_valid_source(
      source=source_name,
      link=link
    )
    if not is_valid_source_link:
      logger.error(f"Ссылки с ресурса \"{source_name}\" не поддерживаются")

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
      logger.exception(f"Ошибка при сохранении ссылки \"{link}\" для пользователя с id \"{user.id}\". Ошибка: {e}")

      await self.session.rollback()

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при сохранении ссылки",
      )

  async def get_all_by(
    self,
    id: int | None = None,
    source_name: SourceName | None = None,
    is_active: bool | None = None,
    user_id: UUID | None = None,
  ) -> Sequence[SearchLinkModel]:
    stmt = (
      select(SearchLinkModel)
      .join(SearchLinkModel.users)
    )

    filters = []
    if id is not None:
      filters.append(SearchLinkModel.id == id)
    if source_name is not None:
      filters.append(SearchLinkModel.source_name == source_name.value)
    if is_active is not None:
      filters.append(SearchLinkModel.is_active == is_active)
    if user_id is not None:
      filters.append(UserModel.id == user_id)

    if filters:
      stmt = stmt.filter(*filters)

    links = await self.session.scalars(stmt)

    return links.all()

  async def edit_one(
    self,
    id: int,
    is_active: bool,
  ) -> SearchLinkModel:
    stmt = (
      update(SearchLinkModel)
      .where(SearchLinkModel.id == id)
      .values(is_active=is_active)
      .returning(SearchLinkModel)
    )

    try:
      model = await self.session.scalar(stmt)

      return model

    except Exception as e:
      logger.exception(f"Ошибка при обновлении ссылки с id \"{id}\". Ошибка: {e}")

      await self.session.rollback()

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при обновлении ссылки",
      )

  async def delete_one(
    self,
    id: int,
  ) -> SearchLinkModel:
    stmt = (
      delete(SearchLinkModel)
      .where(SearchLinkModel.id == id)
      .returning(SearchLinkModel)
    )

    try:
      model = await self.session.scalar(stmt)

      return model

    except Exception as e:
      logger.exception(f"Ошибка при удалении ссылки с id \"{id}\". Ошибка: {e}")

      await self.session.rollback()

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при удалении ссылки",
      )

SearchLinkServiceDependency = Annotated[SearchLinkService, Depends()]
