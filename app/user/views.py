from common.jwt_utils import JWTAuthentication
from common.user_permissions import UserAdminOrOwner
from user.models import User
from user.serializers import UserSerializer, UserPlaySessionSerializer, \
    AuthTokenSerializer, UserDetailSerializer
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate


class UserPlaySessionViewSet(viewsets.ReadOnlyModelViewSet):
    """Return users with their last played game"""
    queryset = User.objects.all()
    serializer_class = UserPlaySessionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class UserViewSet(viewsets.ModelViewSet):
    """Create and retrieve users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        permission_classes = self.permission_classes

        if self.action != 'create' and self.action != 'list':
            permission_classes = [UserAdminOrOwner]
        elif self.action != 'create':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action != 'create':
            self.serializer_class = UserDetailSerializer

        return self.serializer_class


class CreateTokenView(generics.GenericAPIView):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer

    def post(self, request, format=None):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(
            request=request,
            username=email,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate with provided credentials'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return JWTAuthentication.generate_jwt(user.id, user.is_staff)
