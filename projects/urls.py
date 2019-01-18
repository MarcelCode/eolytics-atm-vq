from django.urls import path
from projects import views

urlpatterns = [
    path("<slug:status>/", views.projects, name="projects")
]