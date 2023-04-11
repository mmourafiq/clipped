from typing import Any, Callable, Optional

import orjson


def orjson_dumps(
    obj: Any,
    default: Optional[Callable[[Any], Any]] = ...,
    option: Optional[int] = ...,
) -> str:
    return orjson.dumps(obj, default=default, option=option).decode()
