from rest_framework import viewsets, permissions
from user.models import User
from user.api.v1.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer