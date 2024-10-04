from asyncio import run
from .bot import tg_bot

async def main():
  await tg_bot.start()

if __name__ == "__main__":
  run(main())
