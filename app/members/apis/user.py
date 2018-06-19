from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, UserCreateSerializer, LoginSerializer

User = get_user_model()

__all__ = (
    'SignUp',
    'Login',
    'Logout',
)


class SignUp(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data)


class Logout(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        try:
            request.auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            data = {
                'detail': '토큰이 유효하지 않습니다'
            }
            return Response(data)
        logout(request)
        data = {
            'detail': '정상적으로 로그아웃 되었습니다'
        }
        return Response(data)
