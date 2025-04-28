import os
import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from connect_core.api.mcdr import get_plugin_control_interface
from velocity_helper.config import config_loader, command_loader
from velocity_helper.utils import tr
from velocity_helper.handler import VelocityChatHandler

control_server = None


def on_load(server: PluginServerInterface, prev_module):
    global control_server
    register_handler = True
    rt.plugin_id = server.get_self_metadata().id
    rt.server_dir = server.get_mcdr_config().get("working_directory", None)
    if os.path.exists(os.path.join(rt.server_dir, "server.properties")):
        server.logger.warning(tr(server, "check.server_type"))
        server.logger.error(tr(server, "handler.disable"))
        register_handler = False
    rt.commands = command_loader(server)
    server.logger.info(tr(server, "loader.on_start"))
    config = config_loader(server)
    if config is not None:
        rt.config = config
    else:
        server.logger.error(tr(server,"loader.on_disabled"))
    from velocity_helper.command import command_register, set_server_for_command, set_control_server
    set_server_for_command(server)
    command_register(server)
    if register_handler:
        server.register_server_handler(VelocityChatHandler())
    control_server = get_plugin_control_interface(rt.plugin_id, f"{rt.plugin_id}.entry", server)
    set_control_server(control_server)

def new_connect(server_list):
    """有新的连接"""
    control_server.info(f"子服列表更新为：{server_list}")

def del_connect(server_list):
    """有断开连接"""
    control_server.info(f"子服列表更新为：{server_list}")

def recv_data(server_id: str, data: dict):
    control_server.info(f"Received data from server {server_id}.")
    control_server.info(data.get("message", None))


