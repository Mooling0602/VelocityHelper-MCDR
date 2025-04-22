from typing import Optional
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