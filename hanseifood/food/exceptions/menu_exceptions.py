class MenuNotExistsError(Exception):
    def __init__(self, msg="Today's menu is not exists"):
        super().__init__(msg)