class MissingFieldError(KeyError):
    def __init__(self, field_names, msg="Required arguments named {} are not provided."):
        super().__init__(msg.format(field_names))
