from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, CompanySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Company, Profile

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'owner'
        )
    
class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


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

class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
 
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOwner()]
        return [AllowAny()]
 
    def get_queryset(self):
        return Company.objects.verified().order_by('-rating')
 
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
 
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCompanyOwner()]
 