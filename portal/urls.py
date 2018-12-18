from django.urls import path
from portal import views

urlpatterns = [
    path("<int:project_pk>/", views.project, name="portal"),
    path("download/<int:project_pk>/", views.download, name="download"),
    path("config/<int:project_pk>/", views.config, name="config"),
    ]
