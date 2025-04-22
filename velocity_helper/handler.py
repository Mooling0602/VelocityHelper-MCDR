import re

from typing import List
from typing_extensions import override
from mcdreforged.handler.impl.velocity_handler import VelocityHandler


class VelocityChatHandler(VelocityHandler):
    @override
    def get_stop_command(self) -> str:
        return 'stop'
    
    @classmethod
    def get_player_message_parsing_formatter(cls) -> List[re.Pattern]:
        return [
            re.compile(r'\[(?P<channel>[^\]]+)\]<(?P<name>[^>]+)>\s*(?P<message>.*)')
        ]