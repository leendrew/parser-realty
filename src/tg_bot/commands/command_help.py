from aiogram import Router
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.types import Message
from src.shared import Logger
from .command_types import CommandKey
from ..keyboards.keyboard_menu import get_menu_init_keyboard

logger = Logger().get_instance()

router = Router()

@router.message(Command(CommandKey.help.value))
async def on_command_help_handler(
  message: Message,
) -> None:
  keyboard = get_menu_init_keyboard()
  text = markdown.text(
    # TODO: добавить описание
    "Это бот, just a bot.",
    "Список доступных команд:",
    markdown.hbold("/" + CommandKey.start.value) + " - Старт",
    markdown.hbold("/" + CommandKey.help.value) + " - Информация",
    markdown.hbold("/" + CommandKey.menu.value) + " - Меню",
    markdown.hbold("/" + CommandKey.stop.value) + " - Стоп",
    sep="\n",
  )

  await message.answer(
    text=text,
    reply_markup=keyboard,
  )
