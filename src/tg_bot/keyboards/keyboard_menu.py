from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .keyboard_types import (
  KeyboardMenuKey,
  KeyboardAddLinkKey,
  KeyboardMyLinkKey,
)
from ..callbacks.callback_types import (
  MenuCallbackData,
  AddLinkCallbackData,
  MyLinkCallbackData,
)
from src.models.search_link_model import SearchLinkModel
from src.api.search_links.search_link_types import (
  SearchType,
  search_type_title_map,
)

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
  for link in links:
    link_name = link.name
    is_active = "Активна" if link.is_active else "Неактивна"
    text = f"{link_name} | {is_active}"
    builder.button(
      text=text,
      callback_data=MyLinkCallbackData(
        action=KeyboardMyLinkKey.home,
        id=link.id,
        search_type=link.search_type,
        name=link_name,
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

def get_add_link_keyboard():
  builder = InlineKeyboardBuilder()

  for search_type in SearchType:
    search_type_title = search_type_title_map[search_type]

    builder.button(
      text=search_type_title,
      callback_data=AddLinkCallbackData(
        action=KeyboardAddLinkKey.home,
        search_type=search_type,
      ).pack(),
    )

  builder.button(
    text="Назад",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.home,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()
