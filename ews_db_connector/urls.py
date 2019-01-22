from django.urls import path
from ews_db_connector import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("project/<int:project_pk>/", views.missions_by_project, name="project-missions"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
