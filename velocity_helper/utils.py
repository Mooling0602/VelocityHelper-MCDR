import json

from typing import Any, Callable, Optional
from mcdreforged.api.all import *


def tr(server: PluginServerInterface, key: str, to_str: Optional[bool] = None, **kwargs) -> RTextMCDRTranslation|str:
    try:
        plugin_id = server.get_self_metadata().id
        if not key.startswith("#"):
            result = server.rtr(plugin_id + "." + key, **kwargs)
        else:
            result = server.rtr(key[1:], **kwargs)
        if to_str:
            if to_str is True:
                result = str(result)
        return result
    except Exception as e:
        server.logger.error(e)

def check_data_type(data: dict, type: str) -> bool:
    if data.get('type', None) == type:
        return True
    return False

def load_json(file_path: str) -> dict|list:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def write_to_json(data: dict|list, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Usage: @execute_if(lambda: bool | Callable -> bool)
# Ported from: https://github.com/Mooling0602/MoolingUtils-MCDR/blob/main/mutils/__init__.py
def execute_if(condition: bool | Callable[[], bool]):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            actual_condition = condition() if callable(condition) else condition
            if actual_condition:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator