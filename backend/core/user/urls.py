from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh/', views.refresh_token_view, name='refresh_token'),
    
    # User Statuses
    path('statuses/', views.user_status_list, name='user_status_list'),
    
    # Users CRUD
    path('users/', views.user_list_create, name='user_list_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    
    # Accounts CRUD
    path('accounts/', views.account_list_create, name='account_list_create'),
    path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
    path('accounts/<int:pk>/reset-password/', views.account_reset_password, name='account_reset_password'),
]

