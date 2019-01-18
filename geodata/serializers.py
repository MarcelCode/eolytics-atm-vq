from rest_framework import serializers
from geodata import models


class Landsat8Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Landsat8
        fields = "__all__"


class Sentinel2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sentinel2
        fields = "__all__"


class Sentinel3Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sentinel3
        fields = "__all__"
