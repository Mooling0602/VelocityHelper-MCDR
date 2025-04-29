import os
import re
import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from connect_core.api.mcdr import get_plugin_control_interface
from velocity_helper.config import config_loader, command_loader
from velocity_helper.data import VCHData, VCHDataType
from velocity_helper.utils import tr, load_json, write_to_json
from velocity_helper.handler import VelocityChatHandler

control_server = None
plugin_server: PluginServerInterface = None


def on_load(server: PluginServerInterface, prev_module):
    global control_server, plugin_server
    plugin_server = server
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
    vch_data = VCHData(**data)
    match vch_data.type, vch_data.id:
        case VCHDataType.SEND, "message":
            plugin_server.broadcast(vch_data.content)
        case VCHDataType.REQUEST, "bind":
            path = os.path.join(plugin_server.get_data_folder(), "binds.json")
            name = vch_data.content
            bind_data = []
            if os.path.exists(path):
                bind_data = load_json(path)
            for item in bind_data.copy():
                if item.get(server_id, None) is not None:
                    bind_data.remove(item)
            if name is not None:
                bind_data.append({server_id: name})
            else:
                control_server.error(f"bound server {server_id} failed due to invalid name!")
            write_to_json(bind_data, path)
            control_server.info(f"bound server {server_id} with friendly name {name}.")
        case VCHDataType.EXECUTE, "mcdr_command":
            control_server.info(f"Received mcdr command to execute: {vch_data.content}")
            plugin_server.execute_command(vch_data.content)