from rest_framework import serializers
from geodata import models


class Landsat8Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GeoDataLandsat8
        fields = "__all__"


class Sentinel2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GeoDataSentinel2
        fields = "__all__"


class Sentinel3Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GeoDataSentinel3
        fields = "__all__"
