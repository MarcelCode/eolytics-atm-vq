from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from geodata import views

router = routers.DefaultRouter()
router.register(r'landsat8', views.Landsat8ViewSet)
router.register(r'sentinel2', views.Sentinel2ViewSet)
router.register(r'sentinel3', views.Sentinel3ViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework'))
]
