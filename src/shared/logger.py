import os
import logging

class Logger:
  def __init__(
    self,
    level: int | None = None,
  ) -> None:
    filename = "log.txt"
    dir = "logs"

    is_dir_exist = os.path.exists(dir)
    if not is_dir_exist:
      os.mkdir(dir)
    path = os.path.join(dir, filename)

    logging.basicConfig(
      filename=path,
      filemode="a",
      level=level,
      datefmt="%Y-%m-%d %H:%M:%S",
      format="[%(asctime)s.%(msecs)03d] %(levelname)-7s %(module)s:%(lineno)d - %(message)s",
    )

  def get_instance(self) -> logging.Logger:
    return logging.getLogger(__name__)
