from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from geodata import models



class CountrySerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = models.Country
        geo_field = "geom"
        fields = "__all__"





