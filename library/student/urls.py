from django.urls import path
from . import views

urlpatterns = [
    path('demo', views.demo, name = 'demo'),
    path('lay', views.index, name = 'lay'),
    path('login', views.log_in, name = 'login'),
    path('register', views.register, name = 'register'),
    path('register-edit/<int:id>', views.register_edit, name="register-edit"),
    path('demo', views.demo, name = 'demo'),
    path('branches', views.all_branch, name = 'branches'),
    path('add_branch', views.add_branch, name = 'add_branch'),
    path('edit_branch/<int:id>', views.edit_branch, name = 'edit_branch'),
    path('delete_branch/<int:id>', views.delete_branch, name = 'delete_branch'),
    path('add_semester', views.add_semester, name = 'add_semester'),
]