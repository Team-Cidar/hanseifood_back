from typing import Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from ..jwt.serializers import MyTokenObtainPairSerializer
from ...exceptions.jwt_exceptions import InvalidTokenError, TokenNotProvidedError
from ...models import User


def get_token(user: User) -> Tuple[str, str]:
    token: RefreshToken = MyTokenObtainPairSerializer.get_token(user)
    return str(token), str(token.access_token)


def jwt_authenticate(request: Request) -> Tuple[User, AccessToken]:
    """
    Check if the token is expired or invalid

    Returns
    -------
    Tuple[User, AccessToken]

    See Also
    -------
    This method does
    1. Verify token
        If token is expired, modified, doesn't exists user in database which exists in claims, It'll raise InvalidTokenError.
    2. Token not given
        If token is not given in the header with name 'Authorization', It'll raise TokenNotProvidedError.

    """

    try:
        result = JWTAuthentication().authenticate(request)
        if result is not None:
            return result
        raise TokenNotProvidedError()
    except InvalidToken as e:
        raise InvalidTokenError(e.default_detail)


def verify_token(token: str) -> bool:
    """
    not used. jwt_authentication() does this work
    use when only verification of token is needed
    """
    token_verifier = TokenVerifySerializer(data={'token': token})
    return token_verifier.is_valid(raise_exception=True)