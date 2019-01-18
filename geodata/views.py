from rest_framework import viewsets
from geodata import serializers
from geodata import models
from django.contrib.auth.decorators import login_required


class Landsat8ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Landsat8.objects.all()
    serializer_class = serializers.Landsat8Serializer
    http_method_names = ['get', 'head']


class Sentinel2ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Sentinel2.objects.all()
    serializer_class = serializers.Sentinel2Serializer
    http_method_names = ['get', 'head']


class Sentinel3ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Sentinel3.objects.all()
    serializer_class = serializers.Sentinel3Serializer
    http_method_names = ['get', 'head']
