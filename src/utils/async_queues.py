from typing import Callable
from asyncio import (
  create_task,
  gather,
  sleep,
  Queue,
  Task,
)

SIGTERM = "stop"

class AsyncQueues:
  def __init__(
    self,
    queues_len: int,
    queue_delay: int = 2,
  ) -> None:
    self.__queue_delay = queue_delay
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
      task = await queue.get()
      if task is SIGTERM or not callable(task):
        print(f"Worker \"{name}\" for Queue: {queue} has finished. Task: {task}")
        break

      await task()
      await sleep(self.__queue_delay)
      queue.task_done()

  async def add_task(
    self,
    queue_index: int,
    fn: Callable | str,
  ) -> None:
    task = create_task(fn)
    queue = self.__queues[queue_index]
    await queue.put(task)

    return task

  async def start(self) -> None:
    for index in range(len(self.__queues)):
      name = f"worker {index}"
      queue = self.__queues[index]
      await self.__create_worker(name, queue)

  async def stop(self) -> None:
    tasks: list[Task] = []
    for index in range(len(self.__queues)):
      task = await self.add_task(index, SIGTERM)
      tasks.append(task)

    await gather(*tasks)
