from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user_account):
    """
    Generate JWT tokens for UserAccount model
    
    Args:
        user_account: UserAccount instance
        
    Returns:
        dict: Dictionary containing access and refresh tokens
    """
    refresh = RefreshToken()
    
    refresh['account_id'] = user_account.account_id
    refresh['user_id'] = user_account.user_id
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
