from typing import Any

from ..core.constants.strings.exception_strings import MISSING_REQUEST_FIELD_ERROR
from ..enums.abstract_enum import AbstractEnum
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import DtoFieldTypeError, RequestDataConversionError, DeserializeDataTypeError


class Dto:
    @classmethod
    def deserialize(cls, data: dict) -> Any:
        if not isinstance(data, dict):
            raise DeserializeDataTypeError(data)

        fields: dict = cls.__dict__['__annotations__']

        deserialized_obj: cls = cls.__new__(cls)
        for field, field_type in fields.items():
            try:
                if issubclass(field_type, Dto):
                    setattr(deserialized_obj, field, field_type.deserialize(data[field]))
                elif issubclass(field_type, AbstractEnum):
                    setattr(deserialized_obj, field, field_type.from_name(data[field]))
                elif field_type in (int, float, complex, bool, list, tuple, str, dict):
                    setattr(deserialized_obj, field, field_type(data[field]))
                else:
                    raise DtoFieldTypeError(_type=field_type)
            except KeyError:
                raise MissingFieldError(MISSING_REQUEST_FIELD_ERROR.field_name(list(fields.keys())))
            except ValueError:
                raise RequestDataConversionError(income_data=data[field], dto_type=field_type)
        return deserialized_obj


    @classmethod
    def serialize(cls) -> dict:
        pass
