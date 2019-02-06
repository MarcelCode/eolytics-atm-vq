from django.db import models
from sensor_configs.models import Masking, Config


class MissionActionBlock(models.Model):
    SCENE_CLIPPING = 1
    REGFIL = 2
    LAND_WATER_MASK = 3
    ADJACENCY = 4
    GLINT = 5
    WATER_SPECIES = 6

    CHOICES = [
        (SCENE_CLIPPING, "Scene clipping and masking"),
        (REGFIL, "Regfil"),
        (LAND_WATER_MASK, "Land-Water-Mask"),
        (ADJACENCY, "Adjacency correction"),
        (GLINT, "Glint Correction"),
        (WATER_SPECIES, "Water Species Retrieval")
    ]

    id = models.IntegerField(primary_key=True)
    stop_after_block = models.BooleanField(default=False)
    block_name = models.IntegerField(null=True, blank=True, choices=CHOICES, default=None)
    masking = models.ForeignKey(Masking, blank=True, null=True, on_delete=models.CASCADE)
    config = models.ForeignKey(Config, blank=True, null=True, on_delete=models.CASCADE)
