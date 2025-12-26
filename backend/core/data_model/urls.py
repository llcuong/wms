from django.urls import path
from . import views

app_name = 'data_model'

urlpatterns = [
    path('post-create-factory/', views.post_create_factory, name='post_create_factory'),
    path('post-create-branch/', views.post_create_branch, name='post_create_branch'),
    path('post-create-machine/', views.post_create_machine, name='post_create_machine'),
    path('post-create-machine-line/', views.post_create_machine_line, name='post_create_machine_line'),
    path('get-factory-by-code/', views.get_factory_by_code, name='get_factory_by_code'),
    path('get-branch-by-id/<int:id>/', views.get_branch_by_id, name='get_branch_by_id'),
    path('get-machine-by-id/<int:id>/', views.get_machine_by_id, name='get_machine_by_id'),
    path('get-machine-line-by-id/<int:id>/',  views.get_machine_line_by_id, name='get_machine_line_by_id'),
    path('get-factory-list/', views.get_factory_list, name='get_factory_list'),
    path('get-branch-list/', views.get_branch_list, name='get_branch_list'),
    path('get-machine-list/', views.get_machine_list, name='get_machine_list'),
    path('get-machine-line-list/', views.get_machine_line_list, name='get_machine_line_list'),
    path('update-factory/<str:factory_code>/', views.update_factory, name='update_factory'),
    path('update-branch/<str:branch_code>/', views.update_branch, name='update_branch'),
    path('update-machine/<str:machine_code>/', views.update_machine, name='update_machine'),
    path('update-machine-line/<str:machine_code>/<str:line_code>/', views.update_machine_line, name='update_machine_line'),
    path('delete-factory-by-code/<str:factory_code>/', views.delete_factory_by_code, name='delete_factory_by_code'),
    path('delete-branch-by-code/<str:branch_code>/', views.delete_branch_by_code, name='delete_branch_by_code'),
    path('delete-machine-by-code/<str:machine_code>/', views.delete_machine_by_code, name='delete_machine_by_code'),
    path('delete-machine-line/<str:machine_code>/<str:line_code>/', views.delete_machine_line, name='delete_machine_line'),
]