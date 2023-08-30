class NotAbstractModelError(Exception):
    def __init__(self, msg="It's not a child of AbstractModel"):
        super().__init__(msg)
