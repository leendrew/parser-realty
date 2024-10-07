from asyncio import run, create_task
from src.shared import (
  queues,
  scheduler,
)
from .bot import tg_bot

async def main() -> None:
  create_task(queues.start())
  scheduler.start()
  await tg_bot.start()

if __name__ == "__main__":
  run(main())
