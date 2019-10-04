from django.contrib import admin
from django.urls import path, include
from geodata import views

urlpatterns = [
    path("user-data/", views.geodata_for_user, name="allowed-region"),
    path("aoi-union/", views.check_geodata, name="aoi-union"),
    path("start-download/", views.download_data, name="start-download"),
    path("get-aoi/", views.get_aoi_shape, name="get-aoi")
]
