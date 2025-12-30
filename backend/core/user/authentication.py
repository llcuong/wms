from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserCustomUsers

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        token_version = validated_token.get("token_version", 0)

        print("user_id: ",user_id," --------- token_version: ", token_version)

        if not user_id:
            raise AuthenticationFailed("Token missing user_id")

        try:
            user = UserCustomUsers.objects.select_related('user_status', 'user_account').get(user_id=user_id)
        except UserCustomUsers.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if user.user_account.account_token_version != token_version:
            raise AuthenticationFailed("Token revoked")

        if user.user_status.status_name.lower() != 'active':
            raise AuthenticationFailed("User inactive")

        return user
