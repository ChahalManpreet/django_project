from django.urls import path
from . import views

urlpatterns = [
    path('userLogin', views.userLogin, name="userLogin"),
    path('userRegister', views.userRegister, name="userRegister"),
    path('userLogout', views.userLogout, name="userLogout"),
    path('masterPage', views.masterPage, name="masterPage"),
    path('allBooks', views.allBooks, name="allBooks"),
    path('requestIssueBook/<int:pk>', views.requestIssueBook, name="requestIssueBook"),
    path('requestedBooks', views.requestedBooks, name="requestedBooks"),
    path('booksCategory', views.booksCategory, name="booksCategory"),
]
