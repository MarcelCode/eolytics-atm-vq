from django.urls import path
from portal import views

urlpatterns = [
    path("<slug:sensor>/portal/", views.project, name="portal"),
    path("<slug:sensor>/download-data", views.download, name="download-data"),
    path("<slug:sensor>/config", views.config, name="config"),
    path("<slug:sensor>/config/<int:config_pk>", views.edit_config, name="edit-config"),
    ]
