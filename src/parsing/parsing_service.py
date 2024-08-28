from typing import Annotated
import re
from fastapi import Depends
from bs4 import (
  ResultSet,
  Tag,
  NavigableString,
)
from .parser import Parser
from .fetcher import Fetcher
from src.shared import Logger
from src.api.parsing_results.parsing_result_types import ParsingResult
from src.api.search_links.search_link_types import SourceName
from src.api.parsing_results.parsing_result_types import HousingType

logger = Logger().get_instance()

class ParsingService:
  def __init__(self) -> None:
    self.fetcher = Fetcher()
    self.parser = Parser()

  def parse(
    self,
    source: SourceName,
    link: str,
  ) -> list[ParsingResult]:
    method_by_source = {
      SourceName.avito: self.parse_avito,
      SourceName.yandex: self.parse_yandex,
      SourceName.cian: self.parse_cian,
    }

    method = method_by_source[source]
    if not method:
      logger.error(f"Для источника \"{source}\" не нашлось парсера")

      raise Exception(f"Для источника \"{source}\" не нашлось парсера")

    fetch_response = self.fetcher.get_with_retry(url=link)
    bytes_response = fetch_response.content

    return method(markup=bytes_response)

  def parse_avito(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    item_body_regex = re.compile(r"item-body")
    title_flat_regex = re.compile(r"([^,]+),\s*(\d+(?:[.,]\d+)?).*,\s*([0-9/]+)")
    title_house_regex = re.compile(r"()(\d+).+м²()")
    housing_type_regex = re.compile(r"(квартира)?(комната)?", re.MULTILINE)
    flat_room_type_regex = re.compile(r"(\d+)")
    deposit_regex = re.compile(r"\d+")
    commission_percent_regex = re.compile(r"(\d+)")
    item_metro_station_root_container_regex = re.compile(r"geo-root")
    item_metro_station_icon_regex = re.compile(r"geo-icons")
    specific_geo_map = {
      "мурино": "Девяткино",
    }

    container = body.find(attrs={"data-marker": "catalog-serp"})
    if not container:
      logger.error(f"Не нашел контейнер при парсинге источника \"{SourceName.avito}\"")

      raise Exception(f"Ошибка при парсинге источника \"{SourceName.avito}\"")

    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(attrs={"data-marker": "item"})
    for item in items:
      try:
        item_body = item.find(class_=item_body_regex)

        item_link = item_body.find(attrs={"itemprop": "url"})
        direct_link = "https://www.avito.ru" + item_link.get("href")

        item_title = item_link.find(attrs={"itemprop": "name"})
        title_content = item_title.text.lower()

        # TODO: support Дом 50 м² на участке 2 сот.
        title_match = re.search(pattern=title_regex, string=title_content)
        type, flat_area, floor = title_match.groups()

        housing_type_match = re.search(pattern=housing_type_regex, string=type)
        flat = housing_type_match.group(1)
        room = housing_type_match.group(2)
        housing_type = HousingType.house
        if flat:
          housing_type = HousingType.flat
        if room:
          housing_type = HousingType.room

        flat_room_type_match = re.search(pattern=flat_room_type_regex, string=type)
        flat_room_type = flat_room_type_match and flat_room_type_match.group(1)
        flat_room_type = flat_room_type and int(flat_room_type) or 0

        item_price = item_body.find(attrs={"itemprop": "price"})
        price = int(item_price.get("content"))

        item_params = item_body.find(attrs={"data-marker": "item-specific-params"})
        item_params_text = item_params.text
        arr = item_params_text.split("·")
        deposit_raw = arr[0]
        commission_raw = arr[1]
        
        deposit_matches = re.findall(pattern=deposit_regex, string=deposit_raw)
        deposit = int("".join(deposit_matches))
        deposit_percent = 0
        if deposit:
          deposit_percent = int(deposit / price * 100)

        commission_match = re.search(pattern=commission_percent_regex, string=commission_raw)
        commission = commission_match and commission_match.group(1)
        commission_percent = commission and int(commission) or 0

        metro_station_name = None
        item_metro_station_root_container = item_body.find(class_=item_metro_station_root_container_regex)
        if item_metro_station_root_container:
          item_metro_station_name = item_metro_station_root_container.text.strip().lower()

          if item_metro_station_name in specific_geo_map.keys():
            metro_station_name = specific_geo_map[item_metro_station_name]
          else:
            item_metro_station_name = item_metro_station_root_container.find(class_=item_metro_station_icon_regex)
            metro_station_name = item_metro_station_name.next_sibling.text.strip()

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

      except Exception as e:
        logger.exception(f"При парсинге источника \"{SourceName.avito}\". Ошибка: {e}")

    return result

  def parse_yandex(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    housing_type_regex = re.compile(r"(?:(\d+)?-комн)?(студия)?(комнат)?", re.MULTILINE | re.IGNORECASE)
    flat_area_regex = re.compile(r"(\d+)")
    floor_regex = re.compile(r"\d+")
    price_regex = re.compile(r"\d+")
    metro_station_name_regex = re.compile(r"metrostation__title", re.IGNORECASE)
    tags_regex = re.compile(r"tagscontainer", re.IGNORECASE)
    commission_regex = re.compile(r"комиссия\s+(\d+)?", re.IGNORECASE)
    deposit_regex = re.compile(r"(залог)", re.IGNORECASE)

    container = body.find(class_="OffersSerp__list")
    if not container:
      logger.error(f"Не нашел контейнер при парсинге источника \"{SourceName.yandex}\"")

      raise Exception(f"Ошибка при парсинге источника \"{SourceName.yandex}\"")
    
    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(class_="OffersSerpItem__main")
    for item in items:
      try:
        item_link = item.find(name="a")
        direct_link = "https://realty.ya.ru" + item_link.get("href")

        title_text = item_link.text.strip()
        arr = title_text.split("·")
        flat_area_raw = arr[0]
        housing_type_raw = arr[1]
        floor_raw = arr[2]

        flat_area_match = re.search(pattern=flat_area_regex, string=flat_area_raw)
        flat_area = flat_area_match.group(1)

        # TODO: пофиксить
        flat_room_type = 0
        housing_type = HousingType.house
        housing_type_match = re.search(pattern=housing_type_regex, string=housing_type_raw)
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

        floor_matches = re.findall(pattern=floor_regex, string=floor_raw)
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

      except Exception as e:
        logger.exception(f"При парсинге источника \"{SourceName.yandex}\" что-то пошло не так. Ошибка: {e}")

    return result

  def parse_cian(
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
      logger.error(f"Не нашел контейнер при парсинге источника \"{SourceName.cian}\"")

      raise Exception(f"Ошибка при парсинге источника \"{SourceName.cian}\"")

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

      except Exception as e:
        logger.exception(f"При парсинге источника \"{SourceName.cian}\" что-то пошло не так. Ошибка: {e}")

    return result

ParsingServiceDependency = Annotated[ParsingService, Depends()]
