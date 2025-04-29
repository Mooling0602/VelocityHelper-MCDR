import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from connect_core.api.interface import PluginControlInterface
from velocity_helper.config import DefaultConfig
from velocity_helper.utils import tr


builder = SimpleCommandBuilder()
server: PluginServerInterface = None
control_server = None

def set_server_for_command(s: PluginServerInterface):
    global server
    server = s

def set_control_server(s: PluginControlInterface):
    global control_server
    control_server = s

def command_register(server: PluginServerInterface):
    builder.arg('name', Text)
    builder.arg('server_id', Text)
    builder.register(server)

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin}')
def on_command_main(src: CommandSource, ctx: CommandContext):
    src.reply(
        RTextList(
            tr(server, "command.main", vc=rt.commands.plugin) + "\n",
            tr(server, "command.main_enable", vc=rt.commands.plugin)
        )
    )

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} enable')
def on_command_main_enable(src: CommandSource, ctx: CommandContext):
    if not src.has_permission(4):
        src.reply(tr(server, "permission_denied"))
        return
    if rt.config is not None:
        src.reply(tr(server, "check.plugin_enabled"))
        return
    new_config = DefaultConfig()
    new_config.enabled = True
    server.save_config_simple(new_config)
    server.reload_plugin(rt.plugin_id)

@builder.command(f'{rt.commands.prefix}{rt.commands.server} <name>')
def on_command_server(src: CommandSource, ctx: CommandContext):
    if not src.is_player:
        src.reply(tr(server, "player_only"))
        return
    server_name = ctx['name']
    command = f"send {src.player} {server_name}"
    if control_server.is_server():
        server.execute(command)

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} ping')
def on_command_ping(src: CommandSource, ctx: CommandContext):
    if not src.has_permission_higher_than(2):
        src.reply(tr(server, "permission_denied"))
        return
    clients = control_server.get_server_list()
    for i in clients:
        self_id = control_server.get_server_id()
        if i != self_id:
            control_server.send_data(
                i, rt.plugin_id, {
                    "id": "message",
                    "type": "send",
                    "content": "Ping!"
                }
            )
    src.reply("Ping messages has sent to all clients!")

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} ping <server_id>')
def on_command_ping_server(src: CommandSource, ctx: CommandContext):
    if not src.has_permission_higher_than(2):
        src.reply(tr(server, "permission_denied"))
        return
    server_id = ctx['server_id']
    data = {}
    if server_id != control_server.get_server_id():
        data = {
            "id": "message",
            "type": "send",
            "content": "Ping!"
        }
    else:
        data = {
            "id": "message",
            "type": "send",
            "content": "Ping echo!"
        }
    control_server.send_data(server_id, rt.plugin_id, data)
    src.reply(f"Ping messages has sent to client {server_id}!")

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} bind <name>')
def on_command_bind_server(src: CommandSource, ctx: CommandContext):
    if not src.has_permission(4):
        src.reply(tr(server, "permission_denied"))
        return
    self_id = control_server.get_server_id()
    data = {
        "id": "bind",
        "type": "request",
        "content": ctx['name']
    }
    for i in control_server.get_server_list():
        if i != self_id:
            control_server.send_data(i, rt.plugin_id, data)
    if control_server.is_server() is False:
        control_server.send_data("-----", rt.plugin_id, data)
    src.reply("bind requests has been sent to all other clients!")

@builder.command

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} update_core')
def on_command_update_core(src: CommandSource, ctx: CommandContext):
    if not src.has_permission(4):
        src.reply(tr(server, "permission_denied"))
        return
    data = {
        "id": "mcdr_command",
        "type": "execute",
        "content": "!!MCDR plg install connect_core -U --confirm"
    }
    # control_server.send_data("all", rt.plugin_id, data)
    if not control_server.is_server() is True:
        control_server.send_data("-----", rt.plugin_id, data)
    for i in control_server.get_server_list():
        if i != control_server.get_server_id():
            control_server.send_data(i, rt.plugin_id, data)
    src.reply("Update command is sent, ConnectCore will be updated in all servers.")
    src.reply("Updating ConnectCore locally...")
    server.execute_command("!!MCDR plg install connect_core -U --confirm")