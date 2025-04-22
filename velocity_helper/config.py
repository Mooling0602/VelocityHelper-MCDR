from typing import Optional
from mcdreforged.api.all import *


class DefaultConfig(Serializable):
    enabled: bool = False

class DefaultCommandNodes(Serializable):
    prefix: str = "!!"
    plugin: str = "vc" # 插件相关
    server: str = "server" # 相当于/server
    send: str = "send" # 相当于/send，用法和VC端相同
    
def config_loader(server: PluginServerInterface) -> Optional[Serializable]:
    config: DefaultConfig = server.load_config_simple(target_class=DefaultConfig)
    if config.enabled is not True:
        return None
    else:
        return config
    
def command_loader(server: PluginServerInterface) -> Serializable:
    commands: DefaultCommandNodes = server.load_config_simple(file_name='commands.json', target_class=DefaultCommandNodes)
    return commands