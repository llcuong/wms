from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserAccount, UserCustomUsers
from .serializers import LoginSerializer, LoginResponseSerializer
from .tokens import get_tokens_for_user


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    API endpoint for user login
    
    Request body:
    {
        "account_id": "username",
        "password": "password"
    }
    
    Response:
    {
        "user_id": "U001",
        "account_id": "admin",
        "user_name": "admin",
        "user_full_name": "Administrator",
        "user_email": "admin@example.com",
        "token": "generated_token",
        "last_login": "2025-12-17T14:21:08Z"
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid input',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    account_id = serializer.validated_data['account_id']
    password = serializer.validated_data['password']
    
    try:
        # Find user account
        user_account = UserAccount.objects.get(account_id=account_id)
        
        # Check password
        if not user_account.check_password(password):
            return Response({
                'error': 'Invalid credentials',
                'message': 'Incorrect username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get user details
        try:
            custom_user = UserCustomUsers.objects.get(user_account=user_account)
            
            # Check if user is active
            if custom_user.user_status.status_name.lower() != 'active':
                return Response({
                    'error': 'Account inactive',
                    'message': 'Your account is not active. Please contact administrator.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Update last login
            user_account.update_last_login()
            
            # Generate JWT tokens using custom generator
            tokens = get_tokens_for_user(user_account)
            
            # Prepare response
            response_data = {
                'user_id': custom_user.user_id,
                'account_id': user_account.account_id,
                'user_name': custom_user.user_name,
                'user_full_name': custom_user.user_full_name,
                'user_email': custom_user.user_email or '',
                'access_token': tokens['access'],
                'refresh_token': tokens['refresh'],
                'token_type': 'Bearer',
                'expires_in': 3600,  # 1 hour in seconds
                'last_login': user_account.last_login
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except UserCustomUsers.DoesNotExist:
            return Response({
                'error': 'User not found',
                'message': 'User profile not found. Please contact administrator.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except UserAccount.DoesNotExist:
        return Response({
            'error': 'Invalid credentials',
            'message': 'Incorrect username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'error': 'Server error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    API endpoint for user logout
    Blacklists the refresh token to prevent reuse
    
    Request body:
    {
        "refresh_token": "token_string"
    }
    """
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Invalid token',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    API endpoint to refresh access token using refresh token
    
    Request body:
    {
        "refresh_token": "token_string"
    }
    
    Response:
    {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "token_type": "Bearer",
        "expires_in": 3600
    }
    """
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new tokens from refresh token
        token = RefreshToken(refresh_token)
        
        # Get new access and refresh tokens
        response_data = {
            'access_token': str(token.access_token),
            'refresh_token': str(token),  # New refresh token due to ROTATE_REFRESH_TOKENS
            'token_type': 'Bearer',
            'expires_in': 3600,  # 1 hour in seconds
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Invalid or expired refresh token',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
