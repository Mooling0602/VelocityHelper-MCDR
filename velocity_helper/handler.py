import re
import functools
import parse

from typing import List, Optional
from typing_extensions import override
from mcdreforged.handler.impl.abstract_minecraft_handler import AbstractMinecraftHandler
from mcdreforged.utils.types.message import MessageText
from mcdreforged.info_reactor.server_information import ServerInformation
from mcdreforged.info_reactor.info import Info


class VelocityChatHandler(AbstractMinecraftHandler):
    @override
    def get_stop_command(self) -> str:
        return 'stop' # Velocity目前已支持直接使用stop关闭代理端
    
    @override
    def get_send_message_command(self, target: str, message: MessageText, server_information: ServerInformation) -> Optional[str]:
        return None
    
    @override
    def get_broadcast_message_command(self, message: MessageText, server_information: ServerInformation) -> Optional[str]:
        return None

    # [connected player] Fallen_Breath (/127.0.0.1:12896) has connected
    __player_joined_regex = re.compile(r'\[connected player] (?P<name>[^ ]+) \(/[^ ]+:\d+\) has connected')

    @override
    def parse_player_joined(self, info: Info) -> Optional[str]:
        if not info.is_user:
            if (m := self.__player_joined_regex.fullmatch(info.content)) is not None:
                return m['name']
        return None

    # [connected player] Fallen_Breath (/127.0.0.1:12896) has disconnected
    __player_left_regex = re.compile(r'\[connected player] (?P<name>[^ ]+) \(/[^ ]+:\d+\) has disconnected')

    @override
    def parse_player_left(self, info: Info) -> Optional[str]:
        if not info.is_user:
            if (m := self.__player_left_regex.fullmatch(info.content)) is not None:
                return m['name']
        return None
    
    @override
    def parse_server_version(self, info):
        if not info.is_user:
            m = re.search(r'Booting up (?P<version>Velocity \S+)', info.content)
            if m:
                return m.group('version')
        return None
    
    __server_address_regex = re.compile(r'Listening on /(?P<ip>\S+):(?P<port>\d+)')

    @override
    def parse_server_address(self, info: Info):
        # Listening on /192.168.0.1:25577
        # Listening on /[0:0:0:0:0:0:0:0%0]:25577
        # Listening on /0:0:0:0:0:0:0:0%0:25577
        if not info.is_user:
            if (m := self.__server_address_regex.fullmatch(info.content)) is not None:
                return m['ip'], int(m['port'])
        return None
    
    # Done (3.05s)!
    __server_startup_done_regex = re.compile(r'Done \([0-9.]+s\)!')

    @override
    def test_server_startup_done(self, info: Info) -> bool:
        return not info.is_user and self.__server_startup_done_regex.fullmatch(info.content) is not None

    @override
    def test_rcon_started(self, info: Info) -> bool:
        return False

    @override
    def test_server_stopping(self, info: Info) -> bool:
        # Shutting down the proxy...
        return not info.is_user and info.content == 'Shutting down the proxy...'
    
    @classmethod
    @override
    def get_content_parsing_formatter(cls) -> re.Pattern:
        # It's the same as WaterfallHandler, but since it's a different server here comes an individual copy
        # [00:16:35 INFO] [foo]: bar
        # [00:16:33 WARN]: foo bar
        return re.compile(
            r'\[(?P<hour>\d+):(?P<min>\d+):(?P<sec>\d+) (?P<logging>[^]]+)]'
            r'( \[[^]]+])?'  # useless logger name
            r': (?P<content>.*)'
        )

    @classmethod
    @override
    def get_player_message_parsing_formatter(cls) -> List[re.Pattern]:
        return [
            re.compile(
                r'(\[mcdr:login])?' # 适配Velocity Chat插件
                r'(\[[a-z0-9_:]+])?'
                r'<(?P<name>[^>]+)> (?P<message>.*)'
            )]
    
    @classmethod
    @functools.lru_cache()
    def __get_player_message_parsers(cls) -> List[re.Pattern]:
        """
        The return value is cached for reuse. Do not modify
        """
        # TODO: drop parse.Parser support
        formatters = cls.get_player_message_parsing_formatter()
        return [parse.Parser(fmt) if isinstance(fmt, str) else fmt for fmt in formatters]
    
    def get_name(self) -> str:
        return "velocity_chat_handler"