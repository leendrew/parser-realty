from uuid import UUID
from typing import Annotated
from pydantic import (
  BaseModel,
  model_validator,
)
from fastapi import (
  Query,
  Depends,
)
from src.utils.link_validator import LinkValidator
from .search_link_types import (
  SourceName,
  SearchType,
)

class CreateOnePayloadDto(BaseModel):
  search_type: SearchType
  name: str
  link: str
  source_name: SourceName
  user_id: UUID

  @model_validator(mode="after")
  def validate_link(self):
    is_link_https = LinkValidator.is_valid_https(self.link)
    if not is_link_https:
      raise ValueError("Невалидный протокол")

    link_source = LinkValidator.get_link_source(link=self.link)
    if not link_source:
      raise ValueError("Ссылки с данного сайта не поддерживаются")

    return self

class GetAllByQueryDto(BaseModel):
  id: Annotated[int | None, Query(default=None)] = None
  search_type: Annotated[SearchType | None, Query()] = None
  source_name: Annotated[SourceName | None, Query()] = None
  is_active: Annotated[bool | None, Query()] = None
  user_id: Annotated[UUID | None, Query()] = None

GetAllByQueryDtoDependency = Annotated[GetAllByQueryDto, Depends()]

class EditOnePayloadDto(BaseModel):
  is_active: bool
