from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('get-user-list/', views.get_user_list, name='get_user_list'),
    path('post-login-account/', views.post_login_account, name='post_login_account'),
    path('post-logout-account/', views.post_logout_account, name='post_logout_account'),
    path('post-create-user/', views.post_create_user, name='post_create_user'),
    path('post-create-account/', views.post_create_account, name='post_create_account'),
    path('refresh-access-token/', views.refresh_access_token, name='refresh_access_token'),
]
