from aiogram import (
  Router,
  F,
)
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import MenuCallbackData
from ..keyboards.keyboard_types import KeyboardMenuKey
from ..keyboards.keyboard_menu import (
  get_menu_keyboard,
  get_my_links_keyboard,
  get_no_links_keyboard,
  get_add_link_search_type_keyboard,
)
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.search_links.search_link_service import SearchLinkService

logger = Logger().get_instance()

router = Router()

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.home))
async def on_menu_home_callback_handler(cb_query: CallbackQuery) -> None:
  await cb_query.answer()

  keyboard = get_menu_keyboard()
  text = markdown.text(
    "Это типо меню",
    "Выберите действие",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.my_links))
async def on_menu_my_links_handler(
  cb_query: CallbackQuery,
  user_telegram_service: UserTelegramService,
  search_link_service: SearchLinkService,
) -> None:
  await cb_query.answer()
  tg_user = cb_query.from_user

  telegram_user = await user_telegram_service.get_one(telegram_id=tg_user.id)
  links = await search_link_service.get_all_by(user_id=telegram_user.user_id)
  if not links:
    keyboard = get_no_links_keyboard()
    text = markdown.text(
      "У вас еще нет ссылок",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )
    return

  keyboard = get_my_links_keyboard(links=links)
  text = markdown.text(
    "Ваши ссылки",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.add_link))
async def on_menu_add_link_handler(cb_query: CallbackQuery) -> None:
  await cb_query.answer()

  keyboard = get_add_link_search_type_keyboard()
  text = markdown.text(
    "Выберите, что вы ищете",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
