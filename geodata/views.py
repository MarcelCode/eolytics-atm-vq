from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models import Union
import json
from projects.models import UserProject
from ews_communication import ews_commands
import datetime


def convert_date(date_string):
    date = datetime.datetime.strptime(date_string, "%m/%d/%Y")
    date = date.strftime("%Y%m%d")
    return date


@login_required
def geodata_for_user(request):
    user_profile = Profile.objects.get(pk=request.user.pk)
    geodata = serialize("geojson", user_profile.download_region.all())

    return JsonResponse(geodata, safe=False)


@login_required
def check_geodata(request):
    json_layer_stringified = request.GET.get('aoi')
    mpoly = GEOSGeometry(json_layer_stringified)

    user_profile = Profile.objects.get(pk=request.user.pk)
    user_download_area = user_profile.download_region.all()

    country_layer = user_download_area.filter(geom__intersects=mpoly).aggregate(area=Union('geom'))["area"]
    if country_layer is not None:
        aoi_intersection_layer = mpoly.intersection(country_layer)
        return JsonResponse(aoi_intersection_layer.geojson, safe=False)
    else:
        return JsonResponse({"status": False, "message": "Please draw a rectangle inside your allowed download region.",
                             "title": 'Area of Interest not valid!'})


@login_required
def download_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_project_pk = data.pop("user_project_pk")
        user_project = UserProject.objects.get(pk=int(user_project_pk))
        if user_project.user == request.user:
            data["start_date"] = convert_date(data["start_date"])
            data["end_date"] = convert_date(data["end_date"])

            ews_name = user_project.ews_name
            sensor_id = user_project.sensor.ews_id

            status = ews_commands.download_raw_data(ews_name=ews_name, sensor_id=sensor_id, **data)

            if status:
                return JsonResponse({"type": "success", "status": True,
                                     "message": "Pleas check the download status to get more information.",
                                     "title": 'Download was started!'})

    return JsonResponse({"type": "error", "status": False, "message": "Please try again later.",
                         "title": 'Something went wrong!'})



