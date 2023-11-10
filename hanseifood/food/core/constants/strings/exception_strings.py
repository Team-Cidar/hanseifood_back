class MISSING_ARG_ERROR:
    @staticmethod
    def arg_name(argument_name: str) -> str:
        return f"Required argument named {argument_name} is not provided."

    # override
    def __str__(self):
        raise Exception("call .arg_name() method to use this.")
