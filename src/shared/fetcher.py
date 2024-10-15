from typing import Callable
from asyncio import sleep
from requests import (
  Session,
  Response,
  RequestException,
)
from fake_useragent import FakeUserAgent
from src.shared import Logger

logger = Logger().get_instance()

class Fetcher:
  def __init__(self) -> None:
    self.__requests = Session()
    self.__user_agent = FakeUserAgent(platforms="pc")
    self.__requests.headers = {
      "User-Agent": self.__user_agent.random,
      "Accept": "text/html",
      "Accept-Language": "ru",
    }

  @staticmethod
  async def retry(
    *args,
    fn: Callable[..., Response],
    retries=3,
    delay=1,
    **kwargs,
  ) -> Response | RequestException:
    last_error: RequestException

    for attempt in range(retries):
      try:
        response = fn(*args, **kwargs)

        return response

      except RequestException as e:
        last_error = e
        logger.exception(f"Запрос на парсинг страницы по ссылке упал на попытке: {attempt + 1}")

        if attempt < retries - 1:
          await sleep(delay)

    if (last_error):
      return last_error

  async def get_with_requests(self, *args, **kwargs) -> Response | RequestException:
    result = await self.retry(*args, **kwargs, fn=self.__requests.get)

    return result
