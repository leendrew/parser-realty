from asyncio import run
from .bot import Bot

async def main():
  tg_bot = Bot()
  await tg_bot.start()

if __name__ == "__main__":
  run(main())
