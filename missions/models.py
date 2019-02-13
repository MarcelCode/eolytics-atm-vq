from django.db import models
from sensor_configs.models import Masking, Config


class MissionActionBlock(models.Model):
    RGB_CREATION = 1
    LAND_WATER_MASK = 2
    GLINT_CORRECTION = 3
    PRODUCT_GENERATION = 4

    CHOICES = [
        (RGB_CREATION, "RGB Creation"),
        (LAND_WATER_MASK, "Land-Water-Mask"),
        (GLINT_CORRECTION, "Glint Correction"),
        (PRODUCT_GENERATION, "Product Generation"),
    ]

    id = models.IntegerField(primary_key=True)
    stop_after_block = models.BooleanField(default=False)
    block_name = models.IntegerField(null=True, blank=True, choices=CHOICES, default=None)
    masking = models.ForeignKey(Masking, blank=True, null=True, on_delete=models.CASCADE)
    config = models.ForeignKey(Config, blank=True, null=True, on_delete=models.CASCADE)
