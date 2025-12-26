from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user_custom_user):
    account = user_custom_user.user_account
    refresh = RefreshToken()
    refresh['user_id'] = user_custom_user.user_id
    refresh['account_id'] = account.account_id
    refresh['token_version'] = account.account_token_version
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_access_token(user_custom_user):
    """
    Generate a new access token for the given user.
    """
    account = user_custom_user.user_account
    refresh = RefreshToken()  # Temporarily create a new refresh token object
    refresh['user_id'] = user_custom_user.user_id
    refresh['account_id'] = account.account_id
    refresh['token_version'] = account.account_token_version

    access_token = refresh.access_token
    return str(access_token)

def verify_refresh_token(refresh_token_str):
    """
    Verify refresh token and return user_id if valid.
    Raises TokenError if token invalid or expired.
    """
    try:
        refresh = RefreshToken(refresh_token_str)  # decode token
        user_id = refresh.get('user_id')           # Get user_id from payload
        return user_id
    except TokenError:
        raise