from src.utils.async_queues import AsyncQueues
from src.api.search_links.search_link_types import SourceName 

queues = AsyncQueues(
  queues_len=len(SourceName),
  queue_delay=2,
)
