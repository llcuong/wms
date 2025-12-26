from rest_framework import serializers
from .models import UserCustomUsers, UserStatus


class PostLoginAccountSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        account_id = data.get('account_id')
        password = data.get('password')

        if not account_id or not password:
            raise serializers.ValidationError("Both account_id and password are required.")

        return data

class PostLogoutAccountSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)


class PostCreateUserSerializer(serializers.ModelSerializer):
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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs