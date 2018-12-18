from django.shortcuts import render
from django.shortcuts import redirect
from portal import models
from geodata import models as geomodels
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from portal import forms
from django.core.exceptions import ObjectDoesNotExist


def project(request, project_pk):
    if request.user.is_authenticated:
        projects = models.Project.objects.all()
        actual_project = models.Project.objects.get(pk=project_pk)
        test = [[1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"],
                [1, "mark", "otto", "test", "bla", "neu", "hier", "gehts", "los", "test"]]
        return render(request, "portal/project.html", {"projects": projects, "actual_project": actual_project,
                                                       "scenes": test})

    return redirect("login")


@login_required
def config(request, project_pk):
    actual_project = models.Project.objects.get(pk=project_pk)

    if request.method == "POST":
        settings_form = forms.OrderForm(request.POST)
        if settings_form.is_valid():
            user_default_settings = models.DefaultSettings.objects.filter(user=request.user)
            if user_default_settings.exists():
                user_default_settings[0].product_list.set(settings_form.cleaned_data["product_list"])
                user_default_settings[0].rrs_config.set(settings_form.cleaned_data["rrs_config"])
                user_default_settings[0].save()
                settings_form.cleaned_data.pop("product_list", None)
                settings_form.cleaned_data.pop("rrs_config", None)
                user_default_settings.update(**settings_form.cleaned_data)
            else:
                default_settings = settings_form.save(commit=False)
                default_settings.user = request.user
                default_settings.satellite = actual_project
                default_settings.save()

            return redirect("portal", project_pk=actual_project.pk)
    else:
        if "reset" in request.GET.keys():
            settings_form = forms.OrderForm()
        else:
            try:
                settings_form = forms.OrderForm(instance=models.DefaultSettings.objects.get(user=request.user))
            except:
                settings_form = forms.OrderForm()

    return render(request, "portal/config.html", {"actual_project": actual_project, "form": settings_form})


@login_required
def download(request, project_pk):
    project_object = models.Project.objects.get(pk=project_pk)
    geodata = serialize('geojson', geomodels.Landsat8.objects.all(), geometry_field='geom',
                        fields=("path", "row", "sequence"))
    return render(request, "portal/download.html", {"project": project_object, "geodata": geodata})
