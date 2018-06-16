from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from utils.permissions import IsUserOrReadOnly
from ..serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

__all__ = (
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        elif self.request.method == 'GET':
            return UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'user_pk'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsUserOrReadOnly,
    )
