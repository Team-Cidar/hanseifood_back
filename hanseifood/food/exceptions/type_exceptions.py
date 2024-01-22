class NotDtoClassError(Exception):
    def __init__(self, _type: type, msg="DtoResponse only allows for the data types of 'Dto' or 'Iter[Dto]'. But '{}' is not."):
        super(NotDtoClassError, self).__init__(msg.format(_type.__name__))


class DtoFieldTypeError(Exception):
    def __init__(self, _type: object, msg="Dto field type '{}' is not deserializable. Please check type annotation."):
        super(DtoFieldTypeError, self).__init__(msg.format(_type.__name__))


class RequestDataConversionError(Exception):
    def __init__(self, dto_type: object, income_data, msg="Request data '{}'({}) can't convert to dto field type {}"):
        super(RequestDataConversionError, self).__init__(msg.format(income_data, type(income_data), dto_type))


class DeserializeDataTypeError(Exception):
    def __init__(self, data, msg="Deserialize data type must be a dictionary, but '{}' is type of '{}'"):
        super(DeserializeDataTypeError, self).__init__(msg.format(data, type(data)))


class DynamicTypeError(Exception):
    def __init__(self, field, field_type, msg="TypeError raised while deserializing '{}'<{}>\n"
                                         "check dto field types\n\n"
                                         "Predictable mistakes\n"
                                         "1. set unhashable type as dict key\n"
                                         "2. set Union types"):
        super(DynamicTypeError, self).__init__(msg.format(field, field_type))


class DefaultEnumTypeError(Exception):
    def __init__(self, msg: str = "Improper usage of default enum type 'Enum.NONE'"):
        super(DefaultEnumTypeError, self).__init__(msg)


class NotCallableError(Exception):
    def __init__(self, msg=f"Trying to call not callable object"):
        super(NotCallableError, self).__init__(msg)