from dataclasses import dataclass
from enum import Enum


class VCHDataType(Enum):
    REQUEST = "request"
    SEND = "send"
    EXECUTE = "execute"

@dataclass
class VCHData:
    id: str
    type: VCHDataType
    content: str

    def __post_init__(self):
        if not isinstance(self.type, VCHDataType):
            self.type = VCHDataType(self.type)