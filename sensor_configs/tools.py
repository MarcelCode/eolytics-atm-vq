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


class CustomLayerMapping(LayerMapping):
    def __init__(self, *args, **kwargs):
        self.custom = kwargs.pop('custom', {})
        super(CustomLayerMapping, self).__init__(*args, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(CustomLayerMapping, self).feature_kwargs(feature)
        kwargs.update(self.custom)
        return kwargs


def shp_to_geojson(filepath):
    # read the shapefile
    reader = shapefile.Reader(filepath)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    return dumps({"type": "FeatureCollection", "features": buffer})


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
    return tmpdirname


def handle_shape_upload(form, user_project):
    cleaned_form = form.cleaned_data
    name = cleaned_form["name"]
    file = cleaned_form["file"]

    project_shape_object = UserProjectShape.objects.create(name=name, user_project=user_project)
    tmpdirname = shp_to_db(file, project_shape_object)
    json = serialize("geojson", UserData.objects.filter(user_shape=project_shape_object))
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
    if config.mask_image:
        json_dict["mask_image_name"] = config.mask_image.name
        json_dict["mask_image"] = json.loads(config.imgpart.json_geometry)
    if config.polygonstatistics:
        json_dict["polygonstatistics_name"] = config.polygonstatistics.name
        json_dict["polygonstatistics"] = json.loads(config.polygonstatistics.json_geometry)
    if config.static_mask:
        json_dict["static_mask_name"] = config.static_mask.name
        json_dict["static_mask"] = json.loads(config.static_mask.json_geometry)

    return json_dict