from typing import TYPE_CHECKING, Any, Dict

from clipped.compact.pydantic import PYDANTIC_VERSION, AnyUrl

if TYPE_CHECKING:
    from clipped.compact.pydantic import BaseConfig, ModelField


class Uri(AnyUrl):
    __slots__ = ()

    if PYDANTIC_VERSION.startswith("2."):
        from pydantic_core import core_schema

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type, handler
        ) -> core_schema.CoreSchema:
            from pydantic_core import core_schema

            # Get the core schema for AnyUrl
            schema = handler(AnyUrl)

            # Define a validator that processes the value and returns an instance of Uri
            def validator(value, info):
                value = cls._validate(value)
                if not isinstance(value, cls):
                    value = cls(value)
                return value

            # Wrap the AnyUrl schema with your validator
            return core_schema.with_info_after_validator_function(
                validator,
                schema,
            )

    @classmethod
    def _validate(cls, value: Any):
        if isinstance(value, Dict):
            _value = value.get("user")
            if not _value:
                raise ValueError("Received a wrong url definition: %s", value)
            password = value.get("password")
            if password:
                _value = "{}@{}".format(_value, password)
            host = value.get("host")
            if not host:
                raise ValueError("Received a wrong url definition: %s", value)
            _value = "{}/{}".format(_value, host)
        return value

    @classmethod
    def validate(
        cls, value: Any, field: "ModelField", config: "BaseConfig"
    ) -> "AnyUrl":
        value = cls._validate(value)
        if hasattr(AnyUrl, "validate"):
            return super(Uri, cls).validate(value=value, field=field, config=config)

    def to_param(self):
        return str(self)

    @property
    def host_port(self):
        value = self.host
        if self.port:
            value = "{}:{}".format(value, self.port)
        if self.scheme:
            value = "{}://{}".format(self.scheme, value)
        return value


V1UriType = Uri
