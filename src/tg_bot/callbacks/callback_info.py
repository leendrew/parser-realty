from asyncio import sleep
from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import InfoCallbackData

logger = Logger().get_instance()

router = Router()

@router.callback_query(InfoCallbackData.filter())
async def info_callback_handler(
  cb_query: CallbackQuery,
  callback_data: InfoCallbackData,
) -> None:
  logger.info(f"InfoCallbackData {callback_data}")
  await cb_query.answer()
  tg_user = cb_query.from_user

  await cb_query.message.edit_text("Загрузка...")
  await sleep(5)
  await cb_query.message.edit_text("Загрузка завершена")
