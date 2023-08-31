class EmptyDataError(Exception):
    def __init__(self, msg="Data is not exist"):
        super().__init__(msg)
