import velocity_helper.runtime as rt

from mcdreforged.api.all import *
from velocity_helper.config import DefaultConfig
from velocity_helper.utils import tr


builder = SimpleCommandBuilder()
server = None

def set_server_for_command(s: PluginServerInterface):
    global server
    server = s

def command_register(server: PluginServerInterface):
    builder.arg('name', Text)
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