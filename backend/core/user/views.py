from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from .models import UserAccounts, UserCustomUsers
from .serializers import PostLoginAccountSerializer, PostCreateUserSerializer, PostCreateAccountSerializer, GetUserListSerializer
from .tokens import get_tokens_for_user


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: Change back to IsAuthenticated after testing
def get_user_list(request):
    """
    Get list of all users with their account information.
    
    Response:
    [
        {
            "id": 1,
            "user_id": "USER001",
            "user_name": "johndoe",
            "user_full_name": "John Doe",
            "user_email": "john@example.com",
            "user_status_name": "Active",
            "has_account": true,
            "account": {
                "account_id": "john.doe",
                "account_last_login": "2023-12-01T10:00:00Z",
                "created_at": "2023-01-01T09:00:00Z"
            },
            "created_at": "2023-01-01T09:00:00Z",
            "updated_at": "2023-12-01T10:00:00Z"
        }
    ]
    """
    try:
        users = UserCustomUsers.objects.select_related(
            'user_account', 'user_status'
        ).all().order_by('-created_at')
        
        serializer = GetUserListSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Server error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def post_login_account(request):
    """    
    Request:
    {
        "account_id"
        "password"
    }
    
    Response:
    {
        "user_id"
        "account_id"
        "user_name"
        "user_full_name"
        "user_email"
        "token"
        "last_login"
    }
    """
    serializer = PostLoginAccountSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid input',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    account_id = serializer.validated_data['account_id']
    password = serializer.validated_data['password']

    try:
        # Find user account
        user_account = UserAccounts.objects.get(account_id=account_id)

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
                'expires_in': 3600,
                'last_login': user_account.last_login
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except UserCustomUsers.DoesNotExist:
            return Response({
                'error': 'User not found',
                'message': 'User profile not found. Please contact administrator.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except UserAccounts.DoesNotExist:
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
def post_logout_account(request):
    """
    Request:
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
@permission_classes([IsAuthenticated])
def post_create_user(request):
    serializer = PostCreateUserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save(created_by=request.user.id)

    return Response({
        "message": "User created successfully",
        "user_id": user.user_id
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_account(request):
    serializer = PostCreateAccountSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_id = serializer.validated_data['user_id']
    account_id = serializer.validated_data['account_id']
    password = serializer.validated_data['password']

    try:
        user = UserCustomUsers.objects.get(user_id=user_id)
    except UserCustomUsers.DoesNotExist:
        return Response({
            "error": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if user.user_account:
        return Response({
            "error": "User already has an account"
        }, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        account = UserAccounts(
            user_id=user.user_id,
            account_id=account_id,
            created_by=request.user.id
        )
        account.set_password(password)
        account.save()

        user.user_account = account
        user.save(update_fields=['user_account'])

    return Response({
        "message": "Account created successfully",
        "account_id": account.account_id
    }, status=status.HTTP_201_CREATED)
