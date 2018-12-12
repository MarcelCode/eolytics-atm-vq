from django.urls import path
from portal import views

urlpatterns = [
    path("home/", views.home, name="home"),
    ]
