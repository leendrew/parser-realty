import os
import logging
from src.config import (
  config,
  AppEnv,
)

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

    level_by_env_map = {
      AppEnv.development: None,
      AppEnv.production: logging.ERROR,
    }
    level_by_env = level_by_env_map[config.app.env]
    log_level = level or level_by_env

    logging.basicConfig(
      filename=path,
      filemode="a",
      level=log_level,
      datefmt="%Y-%m-%d %H:%M:%S",
      format="[%(asctime)s.%(msecs)03d] %(levelname)-7s %(module)s:%(lineno)d - %(message)s",
    )

  def get_instance(self) -> logging.Logger:
    return logging.getLogger(__name__)
