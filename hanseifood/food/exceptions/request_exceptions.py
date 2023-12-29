class MissingFieldError(KeyError):
    def __init__(self, msg="Some fields are missing"):
        super().__init__(msg)
