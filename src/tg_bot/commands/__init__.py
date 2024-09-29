from .command_start import router as router_start
from .command_help import router as router_help
from .command_menu import router as router_menu
from .command_stop import router as router_stop
from .ui_commands import ui_commands

commands_routers = [
  router_start,
  router_help,
  router_menu,
  router_stop,
]