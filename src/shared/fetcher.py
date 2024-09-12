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
    self.__instance = Session()
    self.__user_agent = FakeUserAgent()

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

  async def get_with_retry(self, *args, **kwargs) -> Response | RequestException:
    headers = kwargs.get("headers", {})
    headers["user-agent"] = self.__user_agent.random
    kwargs["headers"] = headers

    result = await self.retry(*args, **kwargs, fn=self.__instance.get)

    return result
