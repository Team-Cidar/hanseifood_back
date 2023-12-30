from typing import List


class MISSING_ARG_ERROR:
    @staticmethod
    def arg_name(argument_name: str) -> str:
        return f"Required arguments named {argument_name} is not provided."

    # override
    def __str__(self):
        raise Exception("call .arg_name() method to use MISSING_ARG_ERROR.")


class MISSING_REQUEST_FIELD_ERROR:
    @staticmethod
    def field_name(names: List[str]) -> str:
        return f"Required arguments named {names} is not provided."

    # override
    def __str__(self):
        raise Exception("call .field_name() method to use MISSING_REQUEST_FIELD_ERROR.")