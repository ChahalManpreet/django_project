from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name = ''),
path('login', views.log_in, name = 'login'),
path('register', views.log_in, name = 'register'),
]