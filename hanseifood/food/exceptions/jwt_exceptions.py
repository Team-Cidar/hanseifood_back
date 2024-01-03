class InvalidTokenError(Exception):
    def __init__(self, msg="Token is Invalid"):
        super().__init__(msg)


class PermissionDeniedError(Exception):
    def __init__(self, msg="Permission denied"):
        super().__init__(msg)


class TokenNotProvidedError(Exception):
    def __init__(self, msg="Access token is required. But not given."):
        super().__init__(msg)
