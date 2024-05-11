from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import UserSerializer

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


class RefreshAccessTokenView(views.APIView):
    '''Refresh token view to get a new access token using a refresh token'''
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the refresh token exists and is not blacklisted
            token_instance = OutstandingToken.objects.get(token=refresh_token)
            is_blacklisted = BlacklistedToken.objects.filter(token=token_instance).exists()
            if is_blacklisted:
                return Response({"error": "Token is blacklisted, please login again"}, status=status.HTTP_401_UNAUTHORIZED)
            # Validate the refresh token and get user info
            token = RefreshToken(refresh_token)
            user_id = token['user_id']
            if request.user.is_authenticated and user_id != request.user.id:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            user = get_user_model().objects.get(id=user_id)

            return Response({
                'refresh': str(token),
                'access': str(token.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        except OutstandingToken.DoesNotExist:
            return Response({"error": "Refresh token not found"}, status=status.HTTP_404_NOT_FOUND)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Failed to refresh token"}, status=status.HTTP_400_BAD_REQUEST)

# REFRESH BOTH TOKENS
# class RefreshBothTokensView(views.APIView):
#     '''
#       Create a new refresh token and access token.
#       Blacklist the old refresh token.
#     '''
#     permission_classes = [AllowAny]

#     def post(self, request):
#         refresh_token = request.data.get('refresh')
#         if refresh_token is None:
#             return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Check if the refresh token exists and is not blacklisted
#             token_instance = OutstandingToken.objects.get(token=refresh_token)
#             is_blacklisted = BlacklistedToken.objects.filter(token=token_instance).exists()
#             if is_blacklisted:
#                 return Response({"error": "Token is blacklisted, please login again"}, status=status.HTTP_401_UNAUTHORIZED)
#             # Validate the refresh token and get user info
#             token = RefreshToken(refresh_token)
#             user_id = token['user_id']
#             if request.user.is_authenticated and user_id != request.user.id:
#                 return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

#             user = get_user_model().objects.get(id=user_id)
#             # Blacklist the old refresh token and generate a new one
#             try:
#                 token.blacklist()
#             except TokenError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
#             new_refresh = RefreshToken.for_user(user)

#             return Response({
#                 'refresh': str(new_refresh),
#                 'access': str(new_refresh.access_token),
#                 'user': UserSerializer(user).data
#             }, status=status.HTTP_200_OK)
        
#         except OutstandingToken.DoesNotExist:
#             return Response({"error": "Refresh token not found"}, status=status.HTTP_404_NOT_FOUND)
#         except get_user_model().DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         except TokenError as e:
#             return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({"error": "Failed to refresh token"}, status=status.HTTP_400_BAD_REQUEST)