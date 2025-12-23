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