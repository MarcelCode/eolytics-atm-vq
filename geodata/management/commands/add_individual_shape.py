from django.core.management.base import BaseCommand
from geodata import models
from django.contrib.gis.utils import LayerMapping
import os


class CustomLayerMapping(LayerMapping):
    def __init__(self, *args, **kwargs):
        self.custom = kwargs.pop('custom', {})
        super(CustomLayerMapping, self).__init__(*args, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(CustomLayerMapping, self).feature_kwargs(feature)
        kwargs.update(self.custom)
        return kwargs


class Command(BaseCommand):
    help = 'Add COUNTRY to db'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to Shapefile')
        parser.add_argument('name', type=str, help='Name for Shapefile')

    def handle(self, *args, **kwargs):
        if os.path.isfile(kwargs['filepath']):
            self.save_file(kwargs['filepath'], kwargs['name'])
        else:
            for file in os.listdir(kwargs['filepath']):
                if file.endswith(".shp"):
                    filepath = os.path.join(kwargs['filepath'], file)
                    self.save_file(filepath, kwargs['filepath'])

    @staticmethod
    def save_file(filepath, name):
        layer_map = CustomLayerMapping(
            model=models.Country,
            data=filepath,
            mapping={
                'geom': "MULTIPOLYGON",
            },
            custom={
                "name": name,
                "country_code": "Undefined"
            }
        )

        layer_map.save(progress=True, strict=True)
