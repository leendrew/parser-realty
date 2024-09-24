from src.utils.async_queues import AsyncQueues
# TODO: cycle import
# from src.api.search_links.search_link_types import SourceName

queues = AsyncQueues(
  # queues_len=len(SourceName),
  queues_len=3,
  queue_delay=2,
)
