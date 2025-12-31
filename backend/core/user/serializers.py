from rest_framework import serializers
from .models import UserCustomUsers, UserStatus


class PostLoginAccountSerializer(serializers.Serializer):
    """Serializer for login request."""
    account_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        account_id = data.get('account_id')
        password = data.get('password')

        if not account_id or not password:
            raise serializers.ValidationError("Both account_id and password are required.")

        return data

class PostLogoutAccountSerializer(serializers.Serializer):
    """Serializer for logout request."""
    refresh_token = serializers.CharField(max_length=255)


class PostCreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""
    user_status_id = serializers.PrimaryKeyRelatedField(
        source='user_status',
        queryset=UserStatus.objects.all()
    )

    class Meta:
        model = UserCustomUsers
        fields = [
            'user_id',
            'user_name',
            'user_full_name',
            'user_email',
            'user_status_id'
        ]

class PostCreateAccountSerializer(serializers.Serializer):
    """Serializer for creating a new account."""
    user_id = serializers.CharField(max_length=20)
    account_id = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)


class GetUserAccountSerializer(serializers.Serializer):
    """Serializer for user account information in user list"""
    account_id = serializers.CharField()
    account_last_login = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class GetUserListSerializer(serializers.ModelSerializer):
    """Serializer for getting user list with account info"""
    user_status_name = serializers.CharField(source='user_status.status_name', read_only=True)
    account = serializers.SerializerMethodField()
    has_account = serializers.SerializerMethodField()

    class Meta:
        model = UserCustomUsers
        fields = [
            'id',
            'user_id',
            'user_name',
            'user_full_name',
            'user_email',
            'user_status_name',
            'has_account',
            'account',
            'created_at',
            'updated_at'
        ]

    def get_has_account(self, obj):
        return obj.user_account is not None

    def get_account(self, obj):
        if obj.user_account:
            return GetUserAccountSerializer(obj.user_account).data
        return None

class RefreshAccessTokenResponseSerializer(serializers.Serializer):
    """Serializer for refreshing access token"""
    access_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")
    expires_in = serializers.IntegerField(default=3600)

class ChangeAccountPasswordSerializer(serializers.Serializer):
    """Serializer for changing account password."""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs

class UpdateUserAccountSerializer(serializers.Serializer):
    """
    Serializer PATCH UserAccounts.
    """
    account_password = serializers.CharField(write_only=True, required=False)
    account_last_login = serializers.DateTimeField(required=False)
    account_token_version = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        updated_by = self.context.get('request').user.id if self.context.get('request') else None
        return instance.update_account_safe(updated_by=updated_by, **validated_data)


class UpdateUserCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating UserCustomUsers.
    """
    class Meta:
        model = UserCustomUsers
        fields = [
            'user_name',
            'user_full_name',
            'user_email',
            'user_status',
        ]
        extra_kwargs = {
            'user_name': {'required': False},
            'user_full_name': {'required': False},
            'user_email': {'required': False},
            'user_status': {'required': False},
        }


