from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .models import UserAccounts, UserCustomUsers, UserStatus
from .serializers import (
    LoginSerializer,
    UserStatusSerializer,
    UserAccountListSerializer,
    UserAccountCreateSerializer,
    UserAccountUpdateSerializer,
    ResetPasswordSerializer,
    UserCustomUsersListSerializer,
    UserCustomUsersCreateSerializer,
    UserCustomUsersUpdateSerializer,
)
from .tokens import get_tokens_for_user


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
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
                'expires_in': 3600,  # 1 hour in seconds
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
def logout_view(request):
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
@permission_classes([AllowAny])
def refresh_token_view(request):
    """   
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


# ============== USER STATUS VIEWS ==============
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_status_list(request):
    """Get all user statuses"""
    statuses = UserStatus.objects.all()
    serializer = UserStatusSerializer(statuses, many=True)
    return Response(serializer.data)


# ============== USER VIEWS (CRUD) ==============
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list_create(request):
    """
    GET: List all users
    POST: Create a new user
    """
    if request.method == 'GET':
        users = UserCustomUsers.objects.select_related('user_status', 'user_account').all()
        serializer = UserCustomUsersListSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserCustomUsersCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(created_by=request.user.id if hasattr(request, 'user') else 0)
            return Response(
                UserCustomUsersListSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    """
    GET: Retrieve a user
    PUT: Update a user
    DELETE: Delete a user
    """
    user = get_object_or_404(UserCustomUsers, pk=pk)
    
    if request.method == 'GET':
        serializer = UserCustomUsersListSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserCustomUsersUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save(updated_by=request.user.id if hasattr(request, 'user') else None)
            return Response(UserCustomUsersListSerializer(updated_user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Check if user has associated account
        if hasattr(user, 'user_account') and user.user_account:
            return Response(
                {'error': 'Cannot delete user with associated account. Delete account first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============== ACCOUNT VIEWS (CRUD) ==============
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def account_list_create(request):
    """
    GET: List all accounts
    POST: Create a new account
    """
    if request.method == 'GET':
        accounts = UserAccounts.objects.select_related('account_role').all()
        serializer = UserAccountListSerializer(accounts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserAccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save(created_by=request.user.id if hasattr(request, 'user') else 0)
            # Link account to user if user_id matches
            try:
                user = UserCustomUsers.objects.get(user_id=account.user_id)
                user.user_account = account
                user.save()
            except UserCustomUsers.DoesNotExist:
                pass
            return Response(
                UserAccountListSerializer(account).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def account_detail(request, pk):
    """
    GET: Retrieve an account
    PUT: Update an account
    DELETE: Delete an account
    """
    account = get_object_or_404(UserAccounts, pk=pk)
    
    if request.method == 'GET':
        serializer = UserAccountListSerializer(account)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserAccountUpdateSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            updated_account = serializer.save(updated_by=request.user.id if hasattr(request, 'user') else None)
            return Response(UserAccountListSerializer(updated_account).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Unlink from user first
        try:
            user = UserCustomUsers.objects.get(user_account=account)
            user.user_account = None
            user.save()
        except UserCustomUsers.DoesNotExist:
            pass
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_reset_password(request, pk):
    """
    Reset password for an account
    Request: { "password": "new_password" }
    """
    account = get_object_or_404(UserAccounts, pk=pk)
    serializer = ResetPasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        account.set_password(serializer.validated_data['password'])
        account.updated_by = request.user.id if hasattr(request, 'user') else None
        account.save()
        return Response({'message': 'Password reset successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
