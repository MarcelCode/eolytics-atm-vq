import shapefile
import json
from json import dumps
import tempfile
import os
import zipfile
from django.contrib.gis.utils import LayerMapping
from geodata.models import UserData, UserProjectShape
from django.core.serializers import serialize
import shutil
import geopandas as gpd
from django.contrib import messages


class CustomLayerMapping(LayerMapping):
    def __init__(self, *args, **kwargs):
        self.custom = kwargs.pop('custom', {})
        super(CustomLayerMapping, self).__init__(*args, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(CustomLayerMapping, self).feature_kwargs(feature)
        kwargs.update(self.custom)
        return kwargs


def shp_to_geojson(filepath):
    file = gpd.read_file("/home/marcel/Downloads/test/test.shp")
    file = file.to_crs({'init': 'epsg:4326'})

    return file.to_json()


def shp_to_db(f, project_shape_object):
    tmpdirname = tempfile.mkdtemp()
    filepath = os.path.join(tmpdirname, f.name)

    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(tmpdirname)

    filepath = [os.path.join(tmpdirname, x) for x in os.listdir(tmpdirname) if x.endswith(".shp")][0]

    layer_map = CustomLayerMapping(
        model=UserData,
        data=filepath,
        mapping={
            'geometry': 'MULTIPOLYGON',
        },
        custom={
            'user_shape': project_shape_object
        }
    )
    layer_map.save()

    return tmpdirname, filepath


def handle_shape_upload(form, user_project):
    cleaned_form = form.cleaned_data
    name = cleaned_form["name"]
    file = cleaned_form["file"]

    project_shape_object = UserProjectShape.objects.create(name=name, user_project=user_project)
    tmpdirname, filepath = shp_to_db(file, project_shape_object)
    json = shp_to_geojson(filepath)
    project_shape_object.json_geometry = json
    project_shape_object.save(update_fields=("json_geometry",))

    shutil.rmtree(tmpdirname)


def config_initial(config):
    try:
        initial = config.pk
    except:
        initial = None

    return initial


def serialize_config_model(config):
    json_dict = config.json_configs
    if config.imgpart:
        json_dict["imgpart_name"] = config.imgpart.name
        json_dict["imgpart"] = json.loads(config.imgpart.json_geometry)
    else:
        json_dict["imgpart_name"] = ""
        json_dict["imgpart"] = {}
    if config.mask_image:
        json_dict["mask_image_name"] = config.mask_image.name
        json_dict["mask_image"] = json.loads(config.imgpart.json_geometry)
    else:
        json_dict["mask_image_name"] = ""
        json_dict["mask_image"] = {}
    if config.polygonstatistics:
        json_dict["polygonstatistics_name"] = config.polygonstatistics.name
        json_dict["polygonstatistics"] = json.loads(config.polygonstatistics.json_geometry)
    else:
        json_dict["polygonstatistics_name"] = ""
        json_dict["polygonstatistics"] = {}
    if config.static_mask:
        json_dict["static_mask_name"] = config.static_mask.name
        json_dict["static_mask"] = json.loads(config.static_mask.json_geometry)
    else:
        json_dict["static_mask_name"] = ""
        json_dict["static_mask"] = {}

    return json_dict
