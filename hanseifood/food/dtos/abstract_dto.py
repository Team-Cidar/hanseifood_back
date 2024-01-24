from datetime import datetime
from enum import Enum
from typing import Any, List, Tuple, Dict, Union

from ..core.utils.string_utils import snake_to_camel
from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import DtoFieldTypeError, RequestDataConversionError, DeserializeDataTypeError, \
    DynamicTypeError


class Dto:
    @classmethod
    def deserialize(cls, data: dict) -> Any:
        """
        Deserialize datas to specific type object.
        Dict data -> Instance of Dto

        Allowed field types are
        int, float, bool, list, tuple, str, dict, Enum, Dto, List[T], Tuple[T], Dict[KT, VT]
        """
        if not isinstance(data, dict):
            raise DeserializeDataTypeError(data)

        fields: dict = cls.__annotations__

        deserialized_obj: cls = cls.__new__(cls)
        for field, field_type in fields.items():
            try:
                setattr(deserialized_obj, field, cls.__deserialize_field(field_type, data[snake_to_camel(field)]))
            except KeyError:
                raise MissingFieldError(field_names=[snake_to_camel(field) for field in fields.keys()])
            except ValueError:
                raise RequestDataConversionError(income_data=data[field], dto_type=field_type)
            except TypeError:
                raise DynamicTypeError(field=field, field_type=field_type)
        return deserialized_obj

    def serialize(self) -> dict:
        """
        Serialize instance of Dto class.
        Instance of Dto -> serialized data can be dumped into json
        """
        fields: dict = self.__dict__
        return {snake_to_camel(key): self.__serialize_field(value) for key, value in fields.items()}

    @classmethod
    def serialize_from_iter(cls, datas: Union[list, tuple]):
        return [data.serialize() for data in datas]

    @classmethod
    def __deserialize_field(cls, field_type, data):
        if issubclass(field_type, Dto):  # field: Dto
            return field_type.deserialize(data)
        elif issubclass(field_type, Enum):  # field: Enum
            return field_type(data)
        elif issubclass(field_type, (List, Tuple)):  # field: List[T] | field: Tuple[T]
            subtype: type = field_type.__args__[0]  # T
            base_type: type = field_type.__base__.__base__  # list | tuple
            return base_type([cls.__deserialize_field(subtype, element) for element in data])
        elif issubclass(field_type, Dict):  # field: Dict[KT, VT]
            key_type: type = field_type.__args__[0]  # KT
            value_type: type = field_type.__args__[1]  # VT
            return {key_type(key): cls.__deserialize_field(value_type, value) for key, value in data.items()}
        elif field_type in (int, float, bool, list, tuple, str, dict):  # field: type
            return field_type(data)
        else:
            raise DtoFieldTypeError(_type=field_type)

    def __serialize_field(self, data):
        if isinstance(data, Dto):
            return data.serialize()
        elif isinstance(data, Enum):
            return data.value
        elif isinstance(data, datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, (list, tuple)):
            return [self.__serialize_field(elem) for elem in data]
        elif isinstance(data, dict):
            return {key: self.__serialize_field(value) for key, value in data.items()}
        elif isinstance(data, (int, float, bool, str)):
            return data
        else:
            raise DtoFieldTypeError(_type=type(data), msg="{} is not serializable")
