from django.db import models
from django.contrib.gis.db import models as gismodels
import inspect
import sys


class Landsat8(gismodels.Model):
    path = models.IntegerField()
    row = models.IntegerField()
    sequence = models.IntegerField()
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"row-{self.row}_path-{self.path}"


class Sentinel2(gismodels.Model):
    name = models.CharField(max_length=10)
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"{self.name}"


class Sentinel3(gismodels.Model):
    path = models.IntegerField()
    row = models.IntegerField()
    sequence = models.IntegerField()
    geom = gismodels.PolygonField(srid=4326)

    def __str__(self):
        return f"row-{self.row}_path-{self.path}"


def get_geometry_objects():
    classes = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes[name] = obj

    return classes
