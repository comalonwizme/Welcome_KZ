from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'role': user.profile.role,
                'message': 'Регистрация успешно прошла!',
            }, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username = username, password = password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'role': user.profile.role,
                "message": "Вы успешно вошли!"
            }, status=status.HTTP_200_OK
        )
    return Response(
        {
            "error": "Неверный логин или пароль",
        }, status=status.HTTP_401_UNAUTHORIZED
    )