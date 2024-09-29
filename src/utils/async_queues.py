from typing import Callable
from asyncio import (
  create_task,
  gather,
  sleep,
  Queue,
  Task,
  Future,
)
from src.shared import Logger

logger = Logger().get_instance()

SIGTERM = "stop"

class AsyncQueues:
  def __init__(
    self,
    queues_len: int,
    queue_delay: int = 2,
  ) -> None:
    self.__queue_delay = queue_delay
    self.__workers: list[Task] = []
    self.__queues: list[Queue] = []
    for _ in range(queues_len):
      queue = Queue()
      self.__queues.append(queue)

  async def __create_worker(
    self,
    name: str,
    queue: Queue,
  ) -> None:
    while True:
      fn, args, kwargs, future = await queue.get()

      logger.info(f"{name} has started. Queue len: {queue.qsize()}")

      if fn is SIGTERM:
        logger.info(f"{name} receive sigterm")
        break
      
      result = await fn(*args, **kwargs)
      future.set_result(result)
      logger.info(f"{name} has finished, going to sleep")
      await sleep(self.__queue_delay)
      queue.task_done()

  async def add_task(
    self,
    queue_index: int,
    fn: Callable,
    *args,
    **kwargs,
  ) -> Future:
    if queue_index < 0 or queue_index >= len(self.__queues):
      message = f"Индекс вне доступного диапазона"
      logger.error(message)
      raise ValueError(message)

    queue = self.__queues[queue_index]
    future = Future()
    task_data = (fn, args, kwargs, future)
    await queue.put(task_data)
    logger.info(f"Put task into queue {queue_index}. Queue len: {queue.qsize()}")

    return future

  async def start(self) -> None:
    for index in range(len(self.__queues)):
      name = f"Worker-{index}"
      queue = self.__queues[index]
      worker_task = create_task(self.__create_worker(name, queue))
      self.__workers.append(worker_task)
      logger.info(f"Create {name} for queue {index}")

  async def stop(self) -> None:
    tasks: list[Task] = []
    for queue in self.__queues:
      task = create_task(queue.put((SIGTERM)))
      tasks.append(task)

    await gather(*tasks)
