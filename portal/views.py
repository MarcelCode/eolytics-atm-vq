from django.shortcuts import render
from django.shortcuts import redirect
from portal import models
from geodata import models as geomodels
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from portal import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def project(request, sensor):
    if request.user.is_authenticated:
        projects = models.Sensor.objects.all()
        actual_project = models.Sensor.objects.get(slug=sensor)
        test = [[1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"]
                ]

        sensor_configs = models.get_model_objects()[actual_project.geodata_model]
        configs_per_user = sensor_configs.objects.filter(user=request.user)

        return render(request, "portal/project.html", {"projects": projects, "actual_project": actual_project,
                                                       "scenes": test, "configs": configs_per_user})

    return redirect("login")


@login_required
def config(request, sensor):
    actual_project = models.Sensor.objects.get(slug=sensor)
    config_form = forms.get_form_objects()[actual_project.geodata_model]

    if request.method == "POST":
        config_form_user = config_form(request.POST)
        if config_form_user.is_valid():
            settings = config_form_user.save(commit=False)
            settings.user = request.user
            if "default" in request.POST.keys():
                sensor_configs = models.get_model_objects()[actual_project.geodata_model]
                configs_per_user = sensor_configs.objects.filter(user=request.user)
                configs_per_user.update(default_config=False)
                settings.default_config = True

            settings.save()
            messages.add_message(request, messages.SUCCESS, 'Config was saved')

        return render(request, "portal/config.html", {"actual_project": actual_project, "form": config_form_user})

    return render(request, "portal/config.html", {"actual_project": actual_project, "form": config_form})


@login_required
def edit_config(request, sensor, config_pk):
    actual_project = models.Sensor.objects.get(slug=sensor)
    config_form = forms.get_form_objects()[actual_project.geodata_model]
    sensor_configs = models.get_model_objects()[actual_project.geodata_model]
    user_defined_config = sensor_configs.objects.get(pk=config_pk)

    if request.method == "POST":
        config_form_edited = config_form(request.POST)
        if config_form_edited.is_valid():
            if "default" in request.POST.keys():
                sensor_configs = models.get_model_objects()[actual_project.geodata_model]
                configs_per_user = sensor_configs.objects.filter(user=request.user)
                configs_per_user.update(default_config=False)
                config_form_edited.default_config = True

            config_form_edited.save()
            messages.add_message(request, messages.SUCCESS, 'Config was successfully edited')

        return render(request, "portal/config.html", {"actual_project": actual_project, "form": config_form_edited})

    config_form_user = config_form(instance=user_defined_config)

    return render(request, "portal/config.html", {"actual_project": actual_project, "form": config_form_user})


@login_required
def download(request, sensor):
    project_object = models.Sensor.objects.get(slug=sensor)
    geomodel_object = geomodels.get_geometry_objects()[project_object.geodata_model]

    geodata = serialize('geojson', geomodel_object.objects.all(), geometry_field='geom')
    return render(request, "portal/download.html", {"project": project_object, "geodata": geodata})
