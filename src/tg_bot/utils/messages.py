from aiogram.types import Message
from aiogram.fsm.context import FSMContext

async def remove_last_bot_message_reply_markup(
  message: Message,
  state: FSMContext,
) -> None:
  data = await state.get_data()
  await message.bot.edit_message_reply_markup(
    chat_id=message.chat.id,
    message_id=data["last_bot_message_id"],
    reply_markup=None,
  )
