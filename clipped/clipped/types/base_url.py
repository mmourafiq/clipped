from typing import TYPE_CHECKING, Any
from typing_extensions import Annotated

from clipped.compact.pydantic import PYDANTIC_VERSION, AnyUrl

if TYPE_CHECKING:
    from clipped.compact.pydantic import BaseConfig, ModelField


class BaseUrl(AnyUrl):
    allowed_schemes = []
    __slots__ = ()

    if PYDANTIC_VERSION.startswith("2."):
        from pydantic_core import core_schema

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type, handler
        ) -> core_schema.CoreSchema:
            from pydantic import UrlConstraints
            from pydantic_core import core_schema

            # Get the core schema for AnyUrl
            URLType = Annotated[
                AnyUrl, UrlConstraints(allowed_schemes=cls.allowed_schemes)
            ]
            schema = handler(URLType)

            # Define a validator that processes the value and returns an instance of Uri
            def validator(value, info):
                value = cls._validate(value)
                if not isinstance(value, cls):
                    value = cls(value)
                return value

            return core_schema.with_info_after_validator_function(validator, schema)

    @classmethod
    def validate(
        cls, value: Any, field: "ModelField", config: "BaseConfig"
    ) -> "AnyUrl":
        value = cls._validate(value)
        return super().validate(value=value, field=field, config=config)
