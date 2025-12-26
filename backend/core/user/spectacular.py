from drf_spectacular.extensions import OpenApiAuthenticationExtension
from .authentication import CustomJWTAuthentication

class CustomJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = CustomJWTAuthentication  # class của bạn
    name = "Bearer"