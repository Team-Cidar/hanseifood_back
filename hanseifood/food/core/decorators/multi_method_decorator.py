from rest_framework.request import Request

from ..utils.decorator_utils import get_request_from_args


def multi_methods(GET=None, POST=None, PUT=None, DELETE=None):
    def decorator(_):
        def target_method(*args, **kwargs):
            request: Request = get_request_from_args(*args)
            http_method: str = request.method
            if http_method == 'GET':
                return GET(*args, **kwargs)
            elif http_method == 'POST':
                return POST(*args, **kwargs)
            elif http_method == 'PUT':
                return PUT(*args, **kwargs)
            elif http_method == 'DELETE':
                return DELETE(*args, **kwargs)
        return target_method
    return decorator
