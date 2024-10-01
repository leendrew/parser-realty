from src.api.search_links.search_link_types import (
  SourceName,
  source_name_title_map,
  SearchType,
  search_type_title_map,
)

def __get_supported_sources_text():
  supported_sources = []
  supported_sources.append("Список поддерживающихся источников:")

  for source in SourceName:
    title = source_name_title_map[source]
    text = f"– {title}"
    supported_sources.append(text)

  return supported_sources

supported_sources_text = __get_supported_sources_text()

def __get_search_types_intervals_text():
  interval_text_map = {
    SearchType.rent: "каждые 30 минут",
    SearchType.purchase: "каждый день",
  }
  search_types_intervals = []

  for search_type in SearchType:
    title = search_type_title_map[search_type]
    interval_text = interval_text_map[search_type]
    text = f"– {title} - {interval_text}"
    search_types_intervals.append(text)

  return search_types_intervals

search_types_intervals_text = __get_search_types_intervals_text()
