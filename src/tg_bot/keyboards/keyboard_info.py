from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.shared import Logger
from .keyboard_types import (
  KeyboardMenuKey,
)
from ..callbacks.callback_types import MenuCallbackData

logger = Logger().get_instance()

def get_info_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Меню",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.home,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()
