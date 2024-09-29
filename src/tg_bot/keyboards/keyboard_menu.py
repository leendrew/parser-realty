from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.shared import Logger
from .keyboard_types import (
  KeyboardMenuKey,
  KeyboardMyLinkKey,
)
from ..callbacks.callback_types import (
  MenuCallbackData,
  MyLinkCallbackData,
)
from src.models.search_link_model import SearchLinkModel

logger = Logger().get_instance()

def get_menu_init_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Меню",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.home,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()

def get_menu_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Мои ссылки",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.my_links,
    ).pack(),
  )
  builder.button(
    text="Добавить ссылку",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.add_link,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()

def get_my_links_keyboard(links: list[SearchLinkModel]) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  for index, link in enumerate(links):
    name = link.name or f"Ссылка {index}"
    is_active = "Активна" if link.is_active else "Неактивна"
    text = f"{name} | {is_active}"
    builder.button(
      text=text,
      callback_data=MyLinkCallbackData(
        action=KeyboardMyLinkKey.home,
        id=link.id,
        name=link.name,
        source_name=link.source_name,
        is_active=link.is_active,
      ).pack(),
    )
  builder.button(
    text="Назад",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.home,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()
