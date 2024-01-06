class EmptyDataError(Exception):
    def __init__(self, msg="Data is not exist"):
        super().__init__(msg)


class DBFieldError(ValueError):
    def __init__(self, msg="Required fields are missing"):
        super(DBFieldError, self).__init__(msg)


class AlreadyExistsError(Exception):
    def __init__(self, key, msg="Data with key '{}' is already exists."):
        super(AlreadyExistsError, self).__init__(msg.format(key))