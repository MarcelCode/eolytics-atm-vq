from django.urls import path
from projects import views

urlpatterns = [
    path("projects/<slug:status>/", views.projects, name="projects"),
    path("projects/<slug:status>/remove/<int:project_pk>/", views.delete_project, name="delete-project"),
    path("project/<int:project_pk>/", views.project, name="project"),
    path("project/<int:project_pk>/automatic-mode", views.automatic_mode, name="automatic-mode"),
    path("project/<int:project_pk>/default-settings", views.project_settings, name="project-settings")
]