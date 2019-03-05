from django.urls import path
from ews_db_connector import views

urlpatterns = [
    path("project/test/", views.HelloView.as_view(), name="project-missions"),
]


