from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import secrets

from .models import UserAccount, UserCustomUsers
from .serializers import LoginSerializer, LoginResponseSerializer


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
            
            # Generate simple token (in production, use JWT or Django Rest Framework Token)
            token = secrets.token_urlsafe(32)
            
            # Prepare response
            response_data = {
                'user_id': custom_user.user_id,
                'account_id': user_account.account_id,
                'user_name': custom_user.user_name,
                'user_full_name': custom_user.user_full_name,
                'user_email': custom_user.user_email or '',
                'token': token,
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
def logout_view(request):
    """
    API endpoint for user logout
    This is a placeholder. In production, invalidate the token here.
    """
    return Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)
