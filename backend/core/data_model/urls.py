from django.urls import path
from . import views

app_name = 'data_model'

urlpatterns = [
    path('post_create_factory/', views.post_create_factory, name='post_create_factory'),
    path('post_create_branch/', views.post_create_branch, name='post_create_branch'),
    path('post_create_machine/', views.post_create_machine, name='post_create_machine'),
    path('post_create_machine_line/', views.post_create_machine_line, name='post_create_machine_line'),
    path('get_factory_by_code/', views.get_factory_by_code, name='get_factory_by_code'),
    path('get_branch_by_id/<int:id>/', views.get_branch_by_id, name='get_branch_by_id'),
    path('get_machine_by_id/<int:id>/', views.get_machine_by_id, name='get_machine_by_id'),
    path('get_machine_line_by_id/<int:id>/',  views.get_machine_line_by_id, name='get_machine_line_by_id'),
]