from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_url, name='Home'),
    path('download', views.download, name='Download media'),
]
