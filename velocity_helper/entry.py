import os
import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from velocity_helper.config import config_loader, command_loader
from velocity_helper.utils import tr


def on_load(server: PluginServerInterface, prev_module):
    rt.plugin_id = server.get_self_metadata().id
    rt.server_dir = server.get_mcdr_config().get("working_directory", None)
    if os.path.exists(os.path.join(rt.server_dir, "server.properties")):
        server.logger.warning(tr(server, "check.server_type"))
    rt.commands = command_loader(server)
    server.logger.info(tr(server, "loader.on_start"))
    config = config_loader(server)
    if config is not None:
        rt.config = config
    else:
        server.logger.error(tr(server,"loader.on_disabled"))
    from velocity_helper.command import command_register, set_server_for_command
    set_server_for_command(server)
    command_register(server)


