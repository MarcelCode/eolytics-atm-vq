from django.urls import path
from ews_db_connector import views

urlpatterns = [
    path("project/test/", views.UserProjectView.as_view(), name="test"),
    path("project/<int:project_pk>/", views.ProjectMissionsView.as_view(), name="project-missions")
]


