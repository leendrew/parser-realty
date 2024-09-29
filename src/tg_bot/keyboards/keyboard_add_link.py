from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .keyboard_types import (
  KeyboardAddLinkKey,
  KeyboardMenuKey,
)
from ..callbacks.callback_types import (
  AddLinkCallbackData,
  MenuCallbackData,
)
from src.api.search_links.search_link_types import (
  SourceName,
  source_name_title_map,
)

def get_add_link_init_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Назад",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.add_link,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()

def get_add_link_process_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Сбросить",
    callback_data=AddLinkCallbackData(
      action=KeyboardAddLinkKey.reset,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()

def get_add_link_source_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()

  for source in SourceName:
    source_title = source_name_title_map[source]

    builder.button(
      text=source_title,
      callback_data=AddLinkCallbackData(
        action=KeyboardAddLinkKey.name,
        source_name=source,
      ).pack(),
    )

  builder.button(
    text="Сбросить",
    callback_data=AddLinkCallbackData(
      action=KeyboardAddLinkKey.reset,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()
