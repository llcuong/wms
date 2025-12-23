from rest_framework import serializers
from .models import UserAccounts, UserCustomUsers, UserStatus


class LoginSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        account_id = data.get('account_id')
        password = data.get('password')

        if not account_id or not password:
            raise serializers.ValidationError("Both account_id and password are required.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomUsers
        fields = ['user_id', 'user_name', 'user_full_name', 'user_email']


class LoginResponseSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    account_id = serializers.CharField()
    user_name = serializers.CharField()
    user_full_name = serializers.CharField()
    user_email = serializers.EmailField()
    token = serializers.CharField()
    last_login = serializers.DateTimeField()


# ============== USER STATUS SERIALIZERS ==============
class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['status_id', 'status_name', 'created_at', 'updated_at']
        read_only_fields = ['status_id', 'created_at', 'updated_at']


# ============== USER ACCOUNT SERIALIZERS ==============
class UserAccountListSerializer(serializers.ModelSerializer):
    """Serializer for listing accounts (excludes password)"""
    role_name = serializers.CharField(source='account_role.role_name', read_only=True, allow_null=True)
    
    class Meta:
        model = UserAccounts
        fields = [
            'id', 'user_id', 'account_id', 'account_last_login',
            'account_role', 'role_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'account_last_login', 'created_at', 'updated_at']


class UserAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating accounts (includes password)"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = UserAccounts
        fields = ['user_id', 'account_id', 'password', 'account_role']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        account = UserAccounts(**validated_data)
        account.set_password(password)
        account.save()
        return account


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating accounts (optional password change)"""
    class Meta:
        model = UserAccounts
        fields = ['account_id', 'account_role']


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset"""
    password = serializers.CharField(write_only=True, min_length=6)


# ============== USER CUSTOM USERS SERIALIZERS ==============
class UserCustomUsersListSerializer(serializers.ModelSerializer):
    """Serializer for listing users with related data"""
    user_status = UserStatusSerializer(read_only=True)
    user_account = UserAccountListSerializer(read_only=True)
    
    class Meta:
        model = UserCustomUsers
        fields = [
            'id', 'user_id', 'user_name', 'user_full_name', 'user_email',
            'user_status', 'user_account', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCustomUsersCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users"""
    user_status_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserCustomUsers
        fields = ['user_id', 'user_name', 'user_full_name', 'user_email', 'user_status_id']
    
    def create(self, validated_data):
        status_id = validated_data.pop('user_status_id')
        from .models import UserStatus
        user_status = UserStatus.objects.get(status_id=status_id)
        user = UserCustomUsers.objects.create(user_status=user_status, **validated_data)
        return user


class UserCustomUsersUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating users"""
    user_status_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = UserCustomUsers
        fields = ['user_name', 'user_full_name', 'user_email', 'user_status_id']
    
    def update(self, instance, validated_data):
        status_id = validated_data.pop('user_status_id', None)
        if status_id:
            from .models import UserStatus
            instance.user_status = UserStatus.objects.get(status_id=status_id)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
