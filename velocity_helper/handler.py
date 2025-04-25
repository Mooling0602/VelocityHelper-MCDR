import re

from typing import List
from typing_extensions import override
from mcdreforged.handler.impl.abstract_minecraft_handler import AbstractMinecraftHandler


class VelocityChatHandler(AbstractMinecraftHandler):
    @override
    def get_stop_command(self) -> str:
        return 'stop' # Velocity目前已支持直接使用stop关闭代理端
    
    @classmethod
    @override
    def get_player_message_parsing_formatter(cls) -> List[re.Pattern]:
        return [
            re.compile(
                r'(\[mcdr:login])?' # 适配Velocity Chat插件
                # r'(\[[a-z0-9_:]+])?'
                r'<(?P<name>[^>]+)> (?P<message>.*)'
            )]
    
    def get_name(self) -> str:
        return "velocity_chat_handler"