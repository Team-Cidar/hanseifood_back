from rest_framework.request import Request

def get_request_from_args(*args) -> Request:
    for param in args:
        if isinstance(param, Request):
            return param