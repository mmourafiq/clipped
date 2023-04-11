from typing import Any, Callable, Optional

import orjson


def orjson_dumps(
    obj: Any,
    *,
    default: Optional[Callable[[Any], Any]] = None,
) -> str:
    return orjson.dumps(obj, default=default).decode()

def orjson_dumps_with_options(v: Any, *, default: Optional[Callable[[Any], Any]] = None) -> str:
    return orjson.dumps(
        v, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
    ).decode()
