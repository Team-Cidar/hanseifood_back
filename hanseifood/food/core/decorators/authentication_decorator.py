from typing import List, Tuple
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.request import Request

from ..enums.role_enums import UserRole
from ..utils.jwt_utils import jwt_authenticate
from ...exceptions.jwt_exceptions import InvalidTokenError, PermissionDeniedError, TokenNotProvidedError
from ...models import User
from ...responses.error_response import ErrorResponse


def RequireAuthentication(roles: List[UserRole]):
    def decorator(view_method):
        def authenticate(request: Request) -> Tuple[User, AccessToken]:
            return jwt_authenticate(request)

        def authorization(token: AccessToken):
            if len(roles) == 0:
                return
            payload: dict = token.payload
            role: UserRole = UserRole.from_name(payload['role'])
            if role not in roles:
                raise PermissionDeniedError(f"User's role is '{role}'. But this api required {[str(item) for item in roles]}")

        def get_request(*args):
            for param in args:
                return param if isinstance(param, Request) else None

        def check_token(*args, **kwargs):
            try:
                request: Request = get_request(*args)
                _, token = authenticate(request)
                authorization(token)
                return view_method(*args, **kwargs)
            except TokenNotProvidedError as e:
                return ErrorResponse.response(e, status_code=401)
            except InvalidTokenError as e:
                return ErrorResponse.response(e, status_code=401)
            except PermissionDeniedError as e:
                return ErrorResponse.response(e, status_code=403)
        return check_token
    return decorator
