class NotAbstractModelError(Exception):
    def __init__(self, msg="It's not a child of AbstractModel"):
        super().__init__(msg)


class NotRequestDtoError(Exception):
    def __init__(self, _type: type, msg="Request data class must be a sub class of Dto. But {} is not."):
        super(NotRequestDtoError, self).__init__(msg.format(_type.__name__))


class DtoFieldTypeError(Exception):
    def __init__(self, _type: object, msg="Dto fields must be one of the python's data type or Dto. But '{}' is not."):
        super(DtoFieldTypeError, self).__init__(msg.format(_type.__name__))


class RequestDataConversionError(Exception):
    def __init__(self, dto_type: object, income_data, msg="Request data '{}'({}) can't convert to dto field type {}"):
        super(RequestDataConversionError, self).__init__(msg.format(income_data, type(income_data), dto_type))


class DeserializeDataTypeError(Exception):
    def __init__(self, data, msg="Deserialize data type must be a dictionary, but '{}' is type of '{}'"):
        super(DeserializeDataTypeError, self).__init__(msg.format(data, type(data)))
