from src.api.search_links.search_link_types import (
  SourceName,
  source_name_title_map,
  SearchType,
  search_type_title_map,
)
from ..callbacks.callback_types import MyLinkCallbackPayload

def __get_supported_sources_text() -> list[str]:
  title_text = "Список поддерживающихся источников:"
  supported_sources = []
  supported_sources.append(title_text)

  for source in SourceName:
    title = source_name_title_map[source]
    text = f"– {title}"
    supported_sources.append(text)

  return supported_sources

supported_sources_text = __get_supported_sources_text()

interval_text_map = {
  SearchType.rent: "каждые 30 минут",
  SearchType.purchase: "каждый день",
}

def __get_search_types_intervals_text() -> list[str]:
  title_text = "Уведомления о новых результатах будут приходить:",
  search_types_intervals = []
  search_types_intervals.append(title_text)

  for search_type in SearchType:
    title = search_type_title_map[search_type]
    interval_text = interval_text_map[search_type]
    text = f"– {title} - {interval_text}"
    search_types_intervals.append(text)

  return search_types_intervals

search_types_intervals_text = __get_search_types_intervals_text()

def get_my_link_message(link: MyLinkCallbackPayload) -> list[str]:
  search_type_title = search_type_title_map[link.search_type]
  interval_text = interval_text_map[link.search_type]
  source_name_title = source_name_title_map[link.source_name]
  status_title = "Активна" if link.is_active else "Неактивна"

  title_text = "Информация о ссылке:"
  search_type_text = f"– Тип поиска - {search_type_title}. Уведомления будут приходить {interval_text}"
  name_text = f"– Название - {link.name}"
  source_name_text = f"– Источник - {source_name_title}"
  status_text = f"– Статус - {status_title}"

  return [
    title_text,
    search_type_text,
    name_text,
    source_name_text,
    status_text,
  ]
