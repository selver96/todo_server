from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register-superuser', RegistrationSuperUserView.as_view(), name='register-superuser'),
    path('auth/register', RegistrationView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/is-auth', IsAuthView.as_view(), name='is-auth'),
    path('auth/refresh/token', RefreshTokenView.as_view(), name='refresh-token'),
    path('api/tasks-with-group', TaskGroupAndTaskView.as_view(), name='tasks-with-group'),
    path('api/task-group', TaskGroupView.as_view(), name='task-group'),
    path('api/create-task-group', TaskGroupView.as_view(), name='create-task-group'),
    path('api/delete-task-group/<int:pk>', TaskGroupView.as_view(), name='delete-task-group'),
    path('api/tasks', TaskView.as_view(), name='tasks'),
    path('api/create-tasks', TaskView.as_view(), name='create-tasks'),
    path('api/update-task/<int:pk>', TaskView.as_view(), name='update-task'),
    path('api/delete-task/<int:pk>', TaskView.as_view(), name='update-task'),
    path('api/completed-task/<int:id>', TaskView.as_view(), name='completed-task'),
    
]