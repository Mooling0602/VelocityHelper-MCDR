import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from connect_core.api.interface import PluginControlInterface
from velocity_helper.config import DefaultConfig
from velocity_helper.utils import tr


builder = SimpleCommandBuilder()
server = None
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
    server.execute(f"send {src.player} {server_name}")

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} ping')
def on_command_ping(src: CommandSource, ctx: CommandContext):
    if not src.has_permission_higher_than(2):
        src.reply(tr(server, "permission_denied"))
        return
    clients = control_server.get_server_list()
    for i in clients:
        control_server.send_data(i, rt.plugin_id, {"message": "Ping!"})
    src.reply("Ping messages has sent to all clients!")

@builder.command(f'{rt.commands.prefix}{rt.commands.plugin} ping <server_id>')
def on_command_ping_server(src: CommandSource, ctx: CommandContext):
    if not src.has_permission_higher_than(2):
        src.reply(tr(server, "permission_denied"))
        return
    control_server.send_data(ctx['server_id'], rt.plugin_id, {"message": "Ping!"})
    src.reply(f"Ping messages has sent to client {ctx['server_id']}!")