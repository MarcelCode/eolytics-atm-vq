from django.urls import path
from ews_db_connector import views

urlpatterns = [
    path("project/<int:project_pk>/", views.HelloView.as_view(), name="project-missions"),
]


