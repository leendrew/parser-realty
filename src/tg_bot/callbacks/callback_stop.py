from asyncio import sleep
from aiogram import (
  Router,
  F,
)
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import StopCallbackData
from ..keyboards.keyboard_stop import get_stop_keyboard
from ..keyboards.keyboard_menu import get_menu_keyboard
from ..keyboards.keyboard_types import KeyboardStopKey
from src.api.users.user_service import UserService

logger = Logger().get_instance()

router = Router()

@router.callback_query(StopCallbackData.filter(F.action == KeyboardStopKey.confirm))
async def stop_callback_handler(
  cb_query: CallbackQuery,
  callback_data: StopCallbackData,
  user_service: UserService,
) -> None:
  await cb_query.answer()

  user_summary = await user_service.get_user_summary(id=callback_data.user_id)

  try:
    # TODO: uncomment
    # deleted_user = await user_service.delete_one(id=callback_data.user_id)
    # if not deleted_user:
    #   raise ValueError()

    logger.info(
      f"""
      Пользователь с id {user_summary.id} удален из сервиса.
      Количество ссылок: {user_summary.search_links_count}.
      Количество результатов парсинга: {user_summary.parsing_results_count}
      """
    )
    text = markdown.text(
      "Вы удалены из сервиса",
      "Ваша статистика:",
      f"id - {user_summary.id}",
      f"Количество ссылок - {user_summary.search_links_count}",
      f"Количество результатов парсинга - {user_summary.parsing_results_count}",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
    )

  except Exception:
    keyboard = get_stop_keyboard(user_id=callback_data.user_id)
    text = markdown.text(
      "Произошла ошибка, попробуйте снова",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )

@router.callback_query(StopCallbackData.filter(F.action == KeyboardStopKey.confirm))
async def on_stop_reject_callback_handler(cb_query: CallbackQuery) -> None:
  await cb_query.answer()

  keyboard = get_menu_keyboard()
  text = markdown.text(
    "Действие отменено",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
