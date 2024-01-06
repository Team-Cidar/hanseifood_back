from enum import Enum
from typing import Any, List, Tuple, Dict

from ..exceptions.request_exceptions import MissingFieldError
from ..exceptions.type_exceptions import DtoFieldTypeError, RequestDataConversionError, DeserializeDataTypeError, \
    DynamicTypeError


class Dto:
    @classmethod
    def deserialize(cls, data: dict) -> Any:
        """
        Deserialize datas to specific type object.

        Parameters
        ----------
        data: dict

        Returns
        -------
        Any subclass of RequestDto

        See Also
        -------
        Allowed field types are
        int, float, bool, list, tuple, str, dict, Enum, RequestDto, List[T], Tuple[T], Dict[KT, VT]


        """
        if not isinstance(data, dict):
            raise DeserializeDataTypeError(data)

        fields: dict = cls.__annotations__

        deserialized_obj: cls = cls.__new__(cls)
        for field, field_type in fields.items():
            try:
                setattr(deserialized_obj, field, cls.__deserialize_field(field_type, data[field]))
            except KeyError:
                raise MissingFieldError(field_names=list(fields.keys()))
            except ValueError:
                raise RequestDataConversionError(income_data=data[field], dto_type=field_type)
            except TypeError:
                raise DynamicTypeError(field=field, field_type=field_type)
        return deserialized_obj

    @classmethod
    def __deserialize_field(cls, field_type, data):
        deserialized_field: field_type
        if issubclass(field_type, Dto):  # field: RequestDto
            deserialized_field = field_type.deserialize(data)
        elif issubclass(field_type, Enum):  # field: Enum
            deserialized_field = field_type[data]
        elif issubclass(field_type, (List, Tuple)):  # field: List[T] | field: Tuple[T]
            subtype: type = field_type.__args__[0]  # T
            deserialized_field = field_type.__base__.__base__(
                [cls.__deserialize_field(subtype, element) for element in data]
            )
        elif issubclass(field_type, Dict):  # field: Dict[KT, VT]
            key_type: type = field_type.__args__[0]  # KT
            value_type: type = field_type.__args__[1]  # VT
            deserialized_field = {
                key_type(key): cls.__deserialize_field(value_type, value) for key, value in data.items()
            }
        elif field_type in (int, float, bool, list, tuple, str, dict):  # field: type
            deserialized_field = field_type(data)
        else:
            raise DtoFieldTypeError(_type=field_type)
        return deserialized_field