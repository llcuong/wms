from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('post-login-account/', views.post_login_account, name='post_login_account'),
    path('post-logout-account/', views.post_logout_account, name='post_logout_account'),
    path('post-create-user/', views.post_create_user, name='post_create_user'),
    path('post-create-account/', views.post_create_account, name='post_create_account'),
]
