from django.urls import path
from missions import views

urlpatterns = [
    path("check/", views.check_mission_block, name="check-mission-block"),
    path("action/", views.handle_mission_block, name="handle-mission-block"),
]