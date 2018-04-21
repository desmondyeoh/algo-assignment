from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_path, name='plot_path'),
]