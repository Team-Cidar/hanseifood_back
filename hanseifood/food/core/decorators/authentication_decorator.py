from typing import List, Tuple
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.request import Request

from ..utils import jwt_utils as jwt
from ..utils.decorator_utils import get_request_from_args
from ...enums.role_enums import UserRole
from ...models import User
from ...exceptions.jwt_exceptions import InvalidTokenError, PermissionDeniedError, TokenNotProvidedError
from ...responses.error_response import ErrorResponse


def require_auth(roles: List[UserRole] = UserRole.get_all()):
    def decorator(view_method):
        def __check_user_key() -> bool:
            for key, _type in view_method.__annotations__.items():
                if key == 'user':
                    return True
            return False
        def authenticate(request: Request) -> Tuple[User, AccessToken]:
            return jwt.jwt_authenticate(request)

        def authorize(token: AccessToken, user: User):
            if len(roles) == 0:
                return
            payload: dict = token.payload
            role: UserRole = UserRole.from_value(payload['role'])
            if role.value != str(user.role):
                raise InvalidTokenError("User's role and role in jwt is not same. Please sign in again.")
            if role not in roles:
                raise PermissionDeniedError(f"User's role is '{role}'. But this api required {[str(item) for item in roles]}")

        def check_token(*args, **kwargs):
            try:
                exists_user_key: bool = __check_user_key()

                request: Request = get_request_from_args(*args)
                user, token = authenticate(request)
                authorize(token, user)

                if exists_user_key:
                    kwargs['user'] = user  # allow access to user info in token by using 'user' keyword in view method
                return view_method(*args, **kwargs)
            except TokenNotProvidedError as e:
                return ErrorResponse.response(e, 401)
            except InvalidTokenError as e:
                return ErrorResponse.response(e, 401)
            except AuthenticationFailed as e:
                return ErrorResponse.response(e, 401)
            except PermissionDeniedError as e:
                return ErrorResponse.response(e, 403)
            except Exception as e:
                return ErrorResponse.response(e, 500)

        check_token.__annotations__ = view_method.__annotations__
        return check_token
    return decorator
