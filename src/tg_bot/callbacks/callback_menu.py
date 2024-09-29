from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import MenuCallbackData
from ..keyboards.keyboard_types import KeyboardMenuKey
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.users.user_service import UserService
from src.api.search_links.search_link_service import SearchLinkService

logger = Logger().get_instance()

router = Router()

# @router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.foo))


@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.home))
async def menu_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MenuCallbackData,
  user_telegram_service: UserTelegramService,
  user_service: UserService,
  search_link_service: SearchLinkService,
) -> None:
  logger.info(f"MenuCallbackData {callback_data}")
  await cb_query.answer()
  tg_user = cb_query.from_user

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

  # telegram_user = await user_telegram_service.get_one(telegram_id=tg_user.id)

  # if not telegram_user:
  #   await cb_query.answer(f"Вас нет в системе, для начала введите /start")
  #   return
