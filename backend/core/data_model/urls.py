from django.urls import path
from . import views

urlpatterns = [
    # Factory
    path('factories/', views.factory_list, name='factory-list'),
    path('factories/<str:factory_code>/', views.factory_detail, name='factory-detail'),
    
    # Branch
    path('branches/', views.branch_list, name='branch-list'),
    path('branches/<int:pk>/', views.branch_detail, name='branch-detail'),
    
    # Machine
    path('machines/', views.machine_list, name='machine-list'),
    path('machines/<int:pk>/', views.machine_detail, name='machine-detail'),
    
    # Machine Line
    path('machine-lines/', views.machine_line_list, name='machine-line-list'),
    path('machine-lines/<int:pk>/', views.machine_line_detail, name='machine-line-detail'),
    
    # Roles
    path('roles/', views.role_list, name='role-list'),
    path('roles/<int:pk>/', views.role_detail, name='role-detail'),
    
    # Permissions
    path('permissions/', views.permission_list, name='permission-list'),
    path('permissions/<int:pk>/', views.permission_detail, name='permission-detail'),
    
    # Apps
    path('apps/', views.app_list, name='app-list'),
    path('apps/<int:pk>/', views.app_detail, name='app-detail'),
    
    # App Pages
    path('app-pages/', views.app_page_list, name='app-page-list'),
    path('app-pages/<int:pk>/', views.app_page_detail, name='app-page-detail'),
    
    # Mapping Account Role
    path('mapping-account-roles/', views.mapping_account_role_list, name='mapping-account-role-list'),
    path('mapping-account-roles/<int:pk>/', views.mapping_account_role_detail, name='mapping-account-role-detail'),
    
    # Mapping Account App
    path('mapping-account-apps/', views.mapping_account_app_list, name='mapping-account-app-list'),
    path('mapping-account-apps/<int:pk>/', views.mapping_account_app_detail, name='mapping-account-app-detail'),
    
    # Mapping Account Branch
    path('mapping-account-branches/', views.mapping_account_branch_list, name='mapping-account-branch-list'),
    path('mapping-account-branches/<int:pk>/', views.mapping_account_branch_detail, name='mapping-account-branch-detail'),
]
