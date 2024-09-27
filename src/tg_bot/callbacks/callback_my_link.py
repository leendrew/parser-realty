from asyncio import sleep
from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import MyLinkCallbackData

logger = Logger().get_instance()

router = Router()

@router.callback_query(MyLinkCallbackData.filter())
async def my_link_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
) -> None:
  logger.info(f"MyLinkCallbackData {callback_data}")
  await cb_query.answer()
  tg_user = cb_query.from_user

  await cb_query.message.edit_text("Загрузка...")
  await sleep(5)
  await cb_query.message.edit_text("Загрузка завершена")
