import logging

class Logger:
  def __init__(
    self,
    level: int | None = None,
  ) -> None:
    logging.basicConfig(
      level=level,
      datefmt="%Y-%m-%d %H:%M:%S",
      format="[%(asctime)s.%(msecs)03d] %(levelname)-7s %(module)s:%(lineno)d - %(message)s",
    )

  def get_instance(self) -> logging.Logger:
    return logging.getLogger(__name__)
