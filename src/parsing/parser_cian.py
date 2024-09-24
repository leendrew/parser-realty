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

class ParserCian(ParserBase):
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    container_regex = re.compile(r"cards-wrapper")
    item_regex = re.compile(r"card-wrapper")
    flat_room_type_regex = re.compile(r"(\d+)")
    housing_type_regex = re.compile(r"(студия)?(комната)?", re.MULTILINE | re.IGNORECASE)
    flat_area_regex = re.compile(r"(\d+)")
    floor_regex = re.compile(r"([0-9/]+)")
    price_regex = re.compile(r"\d+")

    container = body.find(class_=container_regex)
    if not container:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.cian}\""
      logger.error(message)
      raise Exception(message)

    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(class_=item_regex)
    for item in items:
      try:
        item_link = item.find(name="a")
        direct_link = item_link.get("href")

        item_title_text = item_link.text.strip()
        arr = item_title_text.split("･")
        house_text_raw = arr[0]
        flat_area_raw = arr[1]
        floor_raw = arr[2]

        flat_room_type = 0
        housing_type = HousingType.house
        flat_room_type_match = re.search(pattern=flat_room_type_regex, string=house_text_raw)
        if flat_room_type_match:
          flat_room_type = int(flat_room_type_match.group(1))
          housing_type = HousingType.flat

        if not flat_room_type_match:
          housing_type_match = re.search(pattern=housing_type_regex, string=house_text_raw)
          studio = housing_type_match.group(1)
          room = housing_type_match.group(2)
          if studio:
            housing_type = HousingType.flat
          if room:
            housing_type = HousingType.room

        flat_area_match = re.search(pattern=flat_area_regex, string=flat_area_raw)
        flat_area = flat_area_match.group(1)

        floor_match = re.search(pattern=floor_regex, string=floor_raw)
        floor = floor_match.group(1)

        metro_station_name = None
        item_metro_station_root_container = item.find(attrs={"data-name": "SpecialGeo"})
        item_metro_station_name_container = item_metro_station_root_container.find(name="a")
        if item_metro_station_name_container:
          metro_station_name = item_metro_station_name_container.text

        item_price_container = item.find(attrs={"data-name": "CardPriceBlock"})
        price_raw = item_price_container.text
        price_matches = re.findall(pattern=price_regex, string=price_raw)
        price = int("".join(price_matches))

        commission_percent = None
        deposit_percent = None

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
        logger.exception(f"При парсинге источника \"{SourceName.cian}\" что-то пошло не так")

    return result
