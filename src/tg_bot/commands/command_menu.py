from aiogram import Router
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.types import Message
from src.shared import Logger
from .command_types import CommandKey
from ..keyboards.keyboard_menu import get_menu_keyboard

logger = Logger().get_instance()

router = Router()

@router.message(Command(CommandKey.menu.value))
async def on_command_menu(
  message: Message,
) -> None:
  keyboard = get_menu_keyboard()
  text = markdown.text(
    "Это типо меню",
    "Выберите действие",
    sep="\n",
  )

  await message.answer(
    text=text,
    reply_markup=keyboard,
  )
