from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'), 
    path('show_result/', views.show_result, name='show_result'),
    path('show_scan/', views.show_scan, name='show_scan'),
    path('check_task_status/', views.check_task_status, name='check_task_status')
]


