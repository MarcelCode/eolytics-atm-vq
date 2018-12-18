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

