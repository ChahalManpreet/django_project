from django.urls import path
from . import views

urlpatterns = [
    
    path('demo', views.demo, name = 'demo'),
    path('lay', views.index, name = 'lay'),
    path('login', views.log_in, name = 'login'),
    path('register', views.register, name = 'register'),
   
    path('branches', views.all_branch, name = 'branches'),
    path('add_branch', views.add_branch, name = 'add_branch'),
    path('edit_branch/<int:id>', views.edit_branch, name = 'edit_branch'),
    path('delete_branch/<int:id>', views.delete_branch, name = 'delete_branch'),

    path('semesters', views.all_semester, name = 'semesters'),
    path('add_semester', views.add_semester, name = 'add_semester'),
    path('edit_semester/<int:id>', views.edit_semester, name = 'edit_semester'),
    path('delete_semester/<int:id>', views.delete_semester, name = 'delete_semester'),

    path('sections', views.all_section, name = 'sections'),
    path('add_section', views.add_section, name = 'add_section'),
    path('edit_section/<int:id>', views.edit_section, name = 'edit_section'),
    path('delete_section/<int:id>', views.delete_section, name = 'delete_section'),

    path('catgorys', views.all_category, name = 'catgorys'),
    path('add_category', views.add_category, name = 'add_category'),
    path('edit_category/<int:id>', views.edit_category, name = 'edit_category'),
    path('delete_category/<int:id>', views.delete_category, name = 'delete_category'),

    path('students', views.all_students, name = 'students'),
    path('add_student', views.add_student, name = 'add_student'),
    #student edit by admin
    path('edit_student/<int:id>', views.edit_student, name='edit_student'),


    path('add_book', views.add_book, name = 'add_book'),
    path('books', views.all_books, name = 'books'),
    path('edit_book/<int:id>', views.edit_book, name='edit_book'),
]