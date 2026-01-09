from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('get-user-list/', views.get_user_list, name='get_user_list'),
    path('post-login-account/', views.post_login_account, name='post_login_account'),
    path('post-logout-account/', views.post_logout_account, name='post_logout_account'),
    path('post-create-user/', views.post_create_user, name='post_create_user'),
    path('post-create-account/', views.post_create_account, name='post_create_account'),
    path('post-refresh-access-token/', views.post_refresh_access_token, name='post_refresh_access_token'),
    path('post-change-account-password/', views.post_change_account_password, name='post_change_account_password'),
    path('patch-account-id/<str:user_id>/', views.patch_account_id, name='patch_account_id'),
    path('delete-user-account/<str:account_id>/', views.delete_user_account, name='delete_user_account'),
    path('patch-user-custom-user/<str:user_id>/', views.patch_user_custom_user, name='patch_user_custom_user'),
    path('get-user-by-user-id/<str:user_id>/', views.get_user_by_user_id, name='get_user_by_user_id'),
    path('get-user-status-list/', views.get_user_status_list, name='get_user_status_list'),
    path('post-update-account-by-user-id/<str:user_id>/', views.post_update_account_by_user_id, name='post_update_account_by_user_id'),
]
