from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dash'),
    path('new_task/', views.create_task, name='new_task'),
    path('new_user_profile/', views.create_user_profile, name='new_profile'),
    path('tasks/<slug:slug>/', views.task_details, name='tasks')
]
