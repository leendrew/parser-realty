from aiogram.fsm.state import (
  StatesGroup,
  State,
)

class AddLinkState(StatesGroup):
  last_bot_message_id = State()
  search_type = State()
  name = State()
  search_link = State()

class MyLinkState(StatesGroup):
  last_bot_message_id = State()
  id = State()
  search_type = State()
  name = State()
  search_link = State()
