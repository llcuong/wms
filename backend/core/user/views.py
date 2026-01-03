from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import UserAccounts, UserCustomUsers
from .serializers import *
# from .tokens import get_tokens_for_user
from .utils import get_tokens_for_user, verify_refresh_token, generate_access_token

#get_user_list Swagger
@extend_schema(
    responses=GetUserListSerializer(many=True),
    tags=["User"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    """
    Get list of all users except the current logged-in user.
    Response:
#     [
#         {
#             "id": 1,
#             "user_id": "USER001",
#             "user_name": "johndoe",
#             "user_full_name": "John Doe",
#             "user_email": "john@example.com",
#             "user_status_name": "Active",
#             "has_account": true,
#             "account": {
#                 "account_id": "john.doe",
#                 "account_last_login": "2023-12-01T10:00:00Z",
#                 "created_at": "2023-01-01T09:00:00Z"
#             },
#             "created_at": "2023-01-01T09:00:00Z",
#             "updated_at": "2023-12-01T10:00:00Z"
#         }
#     ]
    """
    try:
        current_user = request.user  # UserCustomUsers

        users = (
            UserCustomUsers.objects
            .select_related('user_account', 'user_status')
            .exclude(user_id=current_user.user_id)
            .order_by('-created_at')
        )

        serializer = GetUserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {
                'error': 'Server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

#post_login_account Swagger
@extend_schema(
    tags=["Auth"],
    request=PostLoginAccountSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "account_id": {"type": "string"},
                "user_name": {"type": "string"},
                "user_full_name": {"type": "string"},
                "user_email": {"type": "string"},
                "access_token": {"type": "string"},
                # "refresh_token": {"type": "string"},
                "token_type": {"type": "string"},
                "expires_in": {"type": "integer"},
                "last_login": {"type": "string", "format": "date-time"},
            },
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "details": {"type": "object"},
            },
        },
        401: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
        },
        403: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
        },
        500: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
        },
    }
)
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
            # tokens = get_tokens_for_user(user_account)
            tokens = get_tokens_for_user(custom_user)

            # Prepare response
            response_data = {
                'user_id': custom_user.user_id,
                'account_id': user_account.account_id,
                'user_name': custom_user.user_name,
                'user_full_name': custom_user.user_full_name,
                'user_email': custom_user.user_email or '',
                'access_token': tokens['access'],
                # 'refresh_token': tokens['refresh'],
                'token_type': 'Bearer',
                'expires_in': 3600,
                'last_login': user_account.last_login
            }

            response = Response(response_data, status=200)

            # Set the refresh token in an HTTP Only cookie
            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,  # JS can't read
                secure=True,  # send only via HTTPS
                samesite='Strict',
                max_age=7 * 24 * 3600  # 7 days
            )

            # return Response(response_data, status=status.HTTP_200_OK)
            return response

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

# post_logout_account Swagger
@extend_schema(
    tags=["Auth"],
    summary="Logout user",
    description="Invalidate access tokens and refresh token stored in HTTP Only cookie.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        401: {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"}
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_logout_account(request):
    """
    Logout user by invalidating access tokens and refresh token.

    Refresh token is read from HTTP Only cookie; no body required.
    """
    user_account = request.user.user_account
    user_account.account_token_version += 1
    user_account.save(update_fields=['account_token_version'])

    # Get refresh token from HTTP Only cookie
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            print(f"Unexpected error during logout: {str(e)}")

    # Delete refresh token cookie
    response = Response({"message": "Logged out successfully"}, status=200)
    response.delete_cookie('refresh_token')
    return response

#post_create_user Swagger
@extend_schema(
    tags=["User"],
    request=PostCreateUserSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "user_id": {"type": "string"},
            }
        },
        400: {
            "type": "object",
            "properties": {
                "user_id": {"type": "array", "items": {"type": "string"}},
                "user_name": {"type": "array", "items": {"type": "string"}},
                "user_full_name": {"type": "array", "items": {"type": "string"}},
                "user_email": {"type": "array", "items": {"type": "string"}},
                "user_status_id": {"type": "array", "items": {"type": "string"}},
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_user(request):
    """
    Create a new user.
    Request:
    {
        "user_id"
        "user_name"
        "user_full_name"
        "user_email"
        "user_status_id"
    }
    Response:
    {
        "message"
        "user_id"
    }
    """
    serializer = PostCreateUserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save(created_by=request.user.id)

    return Response({
        "message": "User created successfully",
        "user_id": user.user_id
    }, status=status.HTTP_201_CREATED)

#post_create_account Swagger
@extend_schema(
    tags=["User"],
    request=PostCreateAccountSerializer,
    responses={
        201: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "account_id": {"type": "string"},
            }
        },
        400: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_account(request):
    """
    Create a new account for an existing user.
    Request:
    {
        "user_id"
        "account_id"
        "password"
    }
    Response:
    {
        "message"
        "account_id"
    }
    """
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

# refresh_access_token Swagger
@extend_schema(
    tags=["Auth"],
    summary="Refresh access token",
    description=(
        "Refresh the access token using HTTP Only refresh token stored in cookie.\n"
        "No body is required. The server reads the refresh token from cookie."
    ),
    responses={
        200: RefreshAccessTokenResponseSerializer,
        401: {
            "description": "Invalid or expired refresh token",
            "examples": [
                {"error": "Invalid or expired refresh token"}
            ]
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({
            "error": "Refresh token not provided"
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_id = verify_refresh_token(refresh_token)
        user = UserCustomUsers.objects.get(user_id=user_id)
        new_access_token = generate_access_token(user)

        return Response({
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 3600
        }, status=status.HTTP_200_OK)

    except Exception:
        return Response({
            "error": "Invalid or expired refresh token"
        }, status=status.HTTP_401_UNAUTHORIZED)

# change_account_password Swagger
@extend_schema(
    tags=["User"],
    summary="Change password",
    description="Change password for current authenticated user.",
    request=ChangeAccountPasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully"),
        400: OpenApiResponse(description="Invalid input or wrong old password"),
        401: OpenApiResponse(description="Unauthorized"),
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_change_account_password(request):
    """
    Change password for the current authenticated user.
    Request Body:
        {
            "old_password": "old123",
            "new_password": "newStrong123",
            "confirm_password": "newStrong123"
        }
    Rules:
    - old_password must be correct
    - new_password and confirm_password must match
    - token_version will be increased (force re-login)
    """
    serializer = ChangeAccountPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user: UserCustomUsers = request.user
    account = user.user_account

    if not account:
        return Response(
            {"error": "User account not found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check old password
    if not account.check_password(serializer.validated_data["old_password"]):
        return Response(
            {"error": "Old password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Set new password
    account.set_password(serializer.validated_data["new_password"])

    # Invalidate existing tokens
    account.account_token_version += 1
    account.updated_by = user.id if hasattr(user, "id") else None
    account.save(update_fields=["account_password", "account_token_version", "updated_by"])

    return Response(
        {"message": "Password changed successfully"},
        status=status.HTTP_200_OK
    )

# patch_user_account Swagger
@extend_schema(
    tags=["User"],
    request=UpdateUserAccountSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Account updated successfully"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "account_password": {"type": "array", "items": {"type": "string"}},
                "account_last_login": {"type": "array", "items": {"type": "string"}},
                "account_token_version": {"type": "array", "items": {"type": "string"}}
            },
            "example": {
                "account_password": ["This field may not be blank."],
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Account not found"}
            }
        }
    },
    description="Update safe fields of UserAccount: password, token_version, last_login. account_id is not updated to prevent FK errors."
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_user_account(request, account_id):
    """
    Safely update a UserAccount by account_id.
    Path Parameters:
        account_id (string): ID of the UserAccount to be updated.
    Request Body (partial):
        {
            "account_password": "string",
            "account_last_login": "YYYY-MM-DDTHH:MM:SSZ",
            "account_token_version": "integer"
        }
    Responses:
        200 OK:
            Account updated successfully.
            {
                "message": "Account updated successfully"
            }
    """
    try:
        account = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"error": "Account not found"}, status=404)

    serializer = UpdateUserAccountSerializer(account, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Account updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete_user_account Swagger
@extend_schema(
    tags=["User"],
    parameters=[
        OpenApiParameter(
            name='account_id',
            description='ID of the user account to delete',
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        204: {'description': 'Account deleted successfully with cascade on related tables'},
        404: {'description': 'Account not found'}
    },
    description="Delete a UserAccount by its account_id. Cascade deletes all related FK records."
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request, account_id):
    """
    Delete a UserAccount by account_id with cascade on related tables.
    """
    try:
        account = UserAccounts.objects.get(account_id=account_id)
    except UserAccounts.DoesNotExist:
        return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

    account.delete()
    return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# patch_user_custom_user Swagger
@extend_schema(
    tags=["User"],
    request=UpdateUserCustomUserSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "UserCustomUser updated successfully"}
            }
        },
        400: {
            "type": "object",
            "example": {
                "user_email": ["Enter a valid email address."]
            }
        },
        404: {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "UserCustomUser not found"}
            }
        }
    },
    description="Update the safe fields of UserCustomUser. Do not update user_account.user_id to avoid breaking foreign key constraints."
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_user_custom_user(request, user_id):
    """
    Safely update a UserCustomUser by user_id.
    Path Parameters:
        user_id (string): ID of the UserCustomUser to be updated.
    Request Body (partial):
        {
            "user_name": "string",
            "user_full_name": "string",
            "user_email": "string",
            "user_status": "integer"
        }
    Responses:
        200 OK:
            UserCustomUser updated successfully.
            {
                "message": "UserCustomUser updated successfully"
            }
    """
    try:
        user = UserCustomUsers.objects.get(user_id=user_id)
    except UserCustomUsers.DoesNotExist:
        return Response({"error": "UserCustomUser not found"}, status=404)

    serializer = UpdateUserCustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "UserCustomUser updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)