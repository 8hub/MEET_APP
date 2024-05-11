from django.contrib.auth import authenticate
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .serializers import UserSerializer
from rest_framework_simplejwt.exceptions import TokenError

class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        # invalid email
        if 'email' in errors:
            return Response({'error': errors['email']}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # invalid password - to common/ weak/ short/ similar to username
        elif 'password' in errors:
            return Response({'error': errors['password']}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token is None:
                return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            if token.payload['user_id'] != request.user.id:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RefreshTokenView(views.APIView):
    '''Refresh token view to get a new access token using a refresh token'''
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            user = token.user
            if token.blacklisted:
                return Response({"error": "Token is blacklisted, please login again"}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                token.blacklist()
            except TokenError as e:
                return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

            new_refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(new_refresh),
                'access': str(new_refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Failed to refresh token"}, status=status.HTTP_400_BAD_REQUEST)