from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models as geomodels
from geodata.models import UserProjectShape
import os


def get_config_choices():
    configs = os.listdir("templates/configs")
    config_choices = [(x, x.split(".")[0]) for x in configs]

    return config_choices


class Watertype(models.Model):
    ews_id = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["ews_id"]

    def __str__(self):
        return f"{self.name}"


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=100)
    ews_id = models.IntegerField()
    config_name = models.CharField(max_length=255, choices=get_config_choices())
    start_date = models.DateField()

    def __str__(self):
        return f'{self.sensor_name}'


class Config(models.Model):
    user_project = models.ForeignKey("projects.UserProject", on_delete=models.CASCADE)
    ews_ident = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    default = models.BooleanField(default=False)
    json_configs = JSONField()
    imgpart = models.ForeignKey(UserProjectShape, on_delete=models.CASCADE, related_name='imgpart',
                                null=True, blank=True, help_text="Process only a pre-defined area of interest (AOI),"
                                                                 " provided as a ESRI Shapefile.")
    mask_image = models.ForeignKey(UserProjectShape, on_delete=models.CASCADE, related_name='mask_image',
                                   null=True, blank=True, help_text="Mask out regions that shall not be processed by"
                                                                    " defining a precise area of interest, e.g. the"
                                                                    " exact water body you are interested in.",
                                   )
    polygonstatistics = models.ForeignKey(UserProjectShape, on_delete=models.CASCADE, related_name='polygonstatistics',
                                          null=True, blank=True, help_text="Calculate statistics within specific"
                                                                           " regions, defined as single features within"
                                                                           " an ESRI Shapefile.",
                                          )

    static_mask = models.ForeignKey(UserProjectShape, on_delete=models.CASCADE, related_name="static_mask",
                                    null=True, blank=True, help_text="Use static shapes for product masking, "
                                    "e.g. shallow water areas.")

    class Meta:
        unique_together = ("user_project", "name")


class Masking(models.Model):
    user_project = models.ForeignKey("projects.UserProject", on_delete=models.CASCADE)
    ews_ident = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    default = models.BooleanField(default=False)
    json_configs = JSONField()

    class Meta:
        unique_together = ("user_project", "name")

    def __str__(self):
        return f"{self.user_project}, {self.name}, {self.default}"
