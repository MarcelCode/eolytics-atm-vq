from django.core.management.base import BaseCommand
from geodata import models
from django.contrib.gis.utils import LayerMapping
import os


class Command(BaseCommand):
    help = 'Add COUNTRY to db'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to Shapefile')

    def handle(self, *args, **kwargs):
        if os.path.isfile(kwargs['filepath']):
            self.save_file(kwargs['filepath'])
        else:
            for file in os.listdir(kwargs['filepath']):
                if file.endswith(".shp"):
                    filepath = os.path.join(kwargs['filepath'], file)
                    self.save_file(filepath)

    @staticmethod
    def save_file(filepath):
        layer_map = LayerMapping(
            model=models.Country,
            data=filepath,
            mapping={
                "name": "ADMIN",
                "country_code": "ADM0_A3",
                'geom': "MULTIPOLYGON",
            }
        )

        layer_map.save(progress=True, strict=True)
