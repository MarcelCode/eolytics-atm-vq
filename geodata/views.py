from rest_framework import viewsets
from geodata import serializers
from geodata import models
from accounts.models import Profile


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    http_method_names = ['get', 'head']






