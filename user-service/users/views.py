# third party imports
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# standard imports
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer

# Get the custom user model
CustomUser = get_user_model()


# Utility function to create RS256 JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return str(refresh), str(access)


# User Registration View
class UserRegistrationView(APIView):
    """
    Handle user registration and return JWT tokens on success.
    """

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh_token, access_token = get_tokens_for_user(user)
                return Response({
                    'refresh': refresh_token,
                    'access': access_token,
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get Current User View
class GetCurrentUserView(APIView):
    """
    Retrieve the current authenticated user's details.
    """

    def get(self, request):
        try:
            user = request.user
            if user.is_authenticated:
                serializer = RegistrationSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Custom Token Obtain Pair View
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view using RS256 keys.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
