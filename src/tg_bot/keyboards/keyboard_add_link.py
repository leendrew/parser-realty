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
