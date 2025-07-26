from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('create/', views.task_create, name='task-create'),
    path('<int:task_id>/complete/', views.task_complete, name='task-complete'),
    path('<int:task_id>/toggle/', views.task_toggle, name='task-toggle'),
    path('<int:task_id>/start/', views.task_start_timer, name='task-start-timer'),
    path('<int:task_id>/stop/', views.task_stop_timer, name='task-stop-timer'),
]