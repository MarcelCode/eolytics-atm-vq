from django.db import models
from django.contrib.gis.db import models as gismodels
import inspect
import sys


"""
Add geodata for Sensors here
"""


class GeoDataLandsat8(gismodels.Model):
    path = models.IntegerField()
    row = models.IntegerField()
    sequence = models.IntegerField()
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"row-{self.row}_path-{self.path}"


class GeoDataSentinel2(gismodels.Model):
    name = models.CharField(max_length=10)
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"{self.name}"


class GeoDataSentinel3(gismodels.Model):
    path = models.IntegerField()
    row = models.IntegerField()
    sequence = models.IntegerField()
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"row-{self.row}_path-{self.path}"


def get_geodata_names():
    names = [name for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isclass(obj) and
             name.startswith("GeoData")]

    return names
