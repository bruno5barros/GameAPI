import jwt
from datetime import datetime, timedelta
from app.settings import SECRET_KEY
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """Validate if the credentails are valid"""
        token = request.COOKIES.get('jwt')

        if not token:
            token = request.headers.get("token")
            if not token:
                return None

        payload = self.__jwt_decode(token)

        user = self.__validate_user(payload.get('user_id', None),
                                    payload.get('is_staff', None))

        return (user, None)

    @classmethod
    def generate_jwt(cls, id, is_staff):
        """Generate a jwt token"""
        payload = {
            'user_id': id,
            'is_staff': is_staff,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return cls.__create_jwt_cookie(cls, token)

    def __jwt_decode(self, token):
        """Decode and validate the token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        return payload

    def __validate_user(self, user_id, user_is_staff=False):
        """Validate if the user exists"""
        try:
            user = get_user_model().objects.get(
                pk=user_id,
                is_staff=user_is_staff
            )
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return user

    def __create_jwt_cookie(self, token):
        """Create a cookie with the jwt token"""
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {"token": token}
        response.status = status.HTTP_200_OK

        return response
