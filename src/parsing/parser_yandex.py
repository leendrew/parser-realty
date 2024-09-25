import re
from bs4 import (
  ResultSet,
  Tag,
  NavigableString,
)
from src.shared import Logger
from .parser_base import ParserBase
from src.api.parsing_results.parsing_result_types import (
  ParsingResult,
  HousingType,
)
from src.api.search_links.search_link_types import SourceName

logger = Logger().get_instance()

class ParserYandex(ParserBase):
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    housing_type_regex = re.compile(r"(?:(\d+)?-комн)?(студ)?(комнат)?", re.MULTILINE | re.IGNORECASE)
    flat_area_regex = re.compile(r"(\d+)")
    floor_regex = re.compile(r"\d+")
    price_regex = re.compile(r"\d+")
    metro_station_name_regex = re.compile(r"metrostation__title", re.IGNORECASE)
    tags_regex = re.compile(r"tagscontainer", re.IGNORECASE)
    commission_regex = re.compile(r"комиссия\s+(\d+)?", re.IGNORECASE)
    deposit_regex = re.compile(r"(залог)", re.IGNORECASE)

    container = body.find(class_="OffersSerp__list")
    if not container:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.yandex.value}\""
      logger.error(message)
      raise Exception(message)
    
    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(class_="OffersSerpItem__main")
    for item in items:
      try:
        item_link = item.find(name="a")
        direct_link = "https://realty.ya.ru" + item_link.get("href")

        title_text = item_link.text.strip()
        flat_area_raw = ""
        housing_type_raw = ""
        floor_raw = "1"
        arr = title_text.split("·")
        flat_area_raw = arr[0]
        if len(arr) > 1:
          housing_type_raw = arr[1].strip()
          floor_raw = arr[2]

        flat_area_match = re.search(pattern=flat_area_regex, string=flat_area_raw)
        flat_area = flat_area_match.group(1)

        flat_room_type = 0
        housing_type = HousingType.house
        housing_type_match = re.match(pattern=housing_type_regex, string=housing_type_raw)
        if housing_type_match:
          flat = housing_type_match.group(1)
          studio = housing_type_match.group(2)
          room = housing_type_match.group(3)
          if flat:
            flat_room_type = int(flat)
            housing_type = HousingType.flat
          if studio:
            housing_type = HousingType.flat
          if room:
            housing_type = HousingType.room
        if housing_type is HousingType.house:
          flat_room_type = -1

        floor_matches = re.findall(pattern=floor_regex, string=floor_raw)
        if floor_matches:
          floor = "/".join(floor_matches)

        item_price = item.find(class_="Price")
        price_raw = item_price.text
        price_matches = re.findall(pattern=price_regex, string=price_raw)
        price = int("".join(price_matches))

        commission_percent = 0
        deposit_percent = 0
        item_tags_container = item.find(class_=tags_regex)
        tags_raw = item_tags_container.text.strip()

        commission_match = re.search(pattern=commission_regex, string=tags_raw)
        if commission_match:
          commission = commission_match.group(1)
          commission_percent = int(commission)

        deposit_match = re.search(pattern=deposit_regex, string=tags_raw)
        if deposit_match:
          deposit_percent = 100

        metro_station_name = None
        item_metro_station_name = item.find(class_=metro_station_name_regex)
        if item_metro_station_name:
          metro_station_name = item_metro_station_name.text

        parsing_result = ParsingResult(
          direct_link=direct_link,
          housing_type=housing_type,
          flat_room_type=flat_room_type,
          floor=floor,
          flat_area=flat_area,
          price=price,
          commission_percent=commission_percent,
          deposit_percent=deposit_percent,
          metro_station_name=metro_station_name,
        )
        result.append(parsing_result)

      except Exception:
        logger.exception(f"При парсинге источника \"{SourceName.yandex.value}\" что-то пошло не так")

    return result
