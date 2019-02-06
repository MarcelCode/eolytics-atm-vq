from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres.fields import JSONField
from django.core.serializers import serialize


class Country(gismodels.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    geom = gismodels.MultiPolygonField(srid=4326)

    class Meta:
        ordering = ["country_code"]

    def __str__(self):
        return f"{self.country_code} - {self.name}"


class UserData(gismodels.Model):
    user_shape = models.ForeignKey("geodata.UserProjectShape", on_delete=models.CASCADE)
    geometry = gismodels.MultiPolygonField()


class UserProjectShape(models.Model):
    user_project = models.ForeignKey("projects.UserProject", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    json_geometry = JSONField(blank=True, null=True)
