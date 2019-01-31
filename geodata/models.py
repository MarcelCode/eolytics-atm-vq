from django.db import models
from django.contrib.gis.db import models as gismodels


class Country(gismodels.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    geom = gismodels.MultiPolygonField(srid=4326)

    class Meta:
        ordering = ["country_code"]

    def __str__(self):
        return f"{self.country_code} - {self.name}"

