from uuid import UUID
from pydantic import (
  BaseModel,
  ConfigDict,
)
from aiogram.filters.callback_data import CallbackData
from ..keyboards.keyboard_types import (
  KeyboardMenuKey,
  KeyboardAddLinkKey,
  KeyboardMyLinkKey,
  KeyboardStopKey,
)
from src.api.search_links.search_link_types import (
  SourceName,
  SearchType,
)

class MenuCallbackData(
  CallbackData,
  prefix="menu",
):
  action: KeyboardMenuKey

class AddLinkCallbackPayload(BaseModel):
  search_type: SearchType | None = None
  source_name: SourceName | None = None

class AddLinkCallbackData(
  CallbackData,
  AddLinkCallbackPayload,
  prefix="add_link",
):
  action: KeyboardAddLinkKey

class MyLinkCallbackPayload(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int | None = None
  search_type: SearchType | None = None
  name: str | None = None
  source_name: SourceName | None = None
  is_active: bool | None = None

class MyLinkCallbackData(
  CallbackData,
  MyLinkCallbackPayload,
  prefix="my_link",
):
  action: KeyboardMyLinkKey

class StopCallbackPayload(BaseModel):
  user_id: UUID | None = None

class StopCallbackData(
  CallbackData,
  StopCallbackPayload,
  prefix="stop",
):
  action: KeyboardStopKey
