from typing import Any
from uuid import UUID
from pydantic import BaseModel
from aiogram.filters.callback_data import CallbackData
from ..keyboards.keyboard_types import (
  KeyboardMenuKey,
  KeyboardMyLinkKey,
  KeyboardStopKey,
)
from src.api.search_links.search_link_types import SourceName

class MenuCallbackData(
  CallbackData,
  prefix="menu",
):
  action: KeyboardMenuKey

class MyLinkCallbackPayload(BaseModel):
  id: int | None = None
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
