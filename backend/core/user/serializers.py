from rest_framework import serializers
from .models import UserAccounts, UserCustomUsers


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
