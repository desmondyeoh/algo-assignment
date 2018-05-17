from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_path, name='get_path'),
    path('index/', views.index, name='index'),
    path('hi/', views.get_path, name='get_path'),
]