from django.urls import path

from . import views

urlpatterns=[
    path('', views.index, name="index"),
    path('<int:flight_id>', views.fligth, name="flight"),
    path('<int:flight_id>/book', views.book, name="book"),
    path('login', views.loginView, name="loginView"),
    path('logout', views.logoutView, name="logoutView")
]