from rest_framework import serializers


class PostLoginAccountSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        account_id = data.get('account_id')
        password = data.get('password')

        if not account_id or not password:
            raise serializers.ValidationError("Both account_id and password are required.")

        return data
