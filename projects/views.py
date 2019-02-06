from django.shortcuts import render, redirect, HttpResponse
from .models import UserProject
from ews_db_connector.ews_requests import EwsUserQueries
from accounts.models import Profile
from ews_communication import ews_commands
from ews_db_connector import ews_requests
from ews_db_connector.models import DownloadQuery, FileDownload, EwsProject, Mission
from collections import Counter
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from projects import forms
from sensor_configs.models import Config, Masking
from sensor_configs.forms import ConfigForm, MaskingForm, UploadShapeForm, ConfigShapeForm
from sensor_configs import tools
from projects.tools import get_entry_by_pk


def get_filtered_user_projects(project_states, user_projects, status):
    filtered_projects = [ews_name for ews_name, state in project_states.items() if state == status]
    user_projects = user_projects.filter(ews_name__in=filtered_projects)

    return user_projects


@login_required
def projects(request, status):
    create_project_form = forms.CreateProjectForm(user=request.user)
    if request.method == "POST":
        user_project_form = forms.CreateProjectForm(request.user, request.POST)
        if user_project_form.is_valid():
            # EWS Command
            user_info = Profile.objects.get(user=request.user)
            form = user_project_form.cleaned_data
            ews_region = user_info.region_code + form["region"].replace("-", "").replace(" ", "").replace("_", "")
            ews_name = ews_commands.create_ews_project(user_project_name=form['user_project_name'],
                                                       project_abbrevation=form['project_abbrevation'],
                                                       sensor_id=form['sensor'].ews_id,
                                                       watertype=form["watertype"].ews_id,
                                                       region=ews_region,
                                                       project=user_info.project_name)

            if ews_name:
                cleaned_form = user_project_form.cleaned_data
                user_project = UserProject(user=request.user, ews_name=ews_name, **cleaned_form)
                user_project.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Your Project was added successfully!',
                                     extra_tags='alert-success')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Error! Please try again.',
                                     extra_tags='alert-danger')

    user_projects = UserProject.objects.filter(user=request.user)
    ews_queries = ews_requests.EwsUserQueries()
    project_states = ews_queries.get_states_for_projects(user_projects)
    state_count = Counter(project_states.values())
    state_count["all"] = len(user_projects)

    if status == "running" or status == "failed":
        user_projects = get_filtered_user_projects(project_states, user_projects, status)

    # temporarily add states to projects
    for project_object in user_projects:
        project_object.state = project_states[project_object.ews_name]

    return render(request, "projects/projects.html", {"form": create_project_form, "status": status,
                                                      "project_states": project_states, "table": user_projects,
                                                      "state_count": state_count})


@login_required
def delete_project(request, status, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    ews_commands.remove_ews_project(ews_project.ews_name)

    ews_project.delete()

    return redirect("projects", status)


@login_required
def project(request, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    config = Config.objects.get(user_project=ews_project, default=True)
    masking = Masking.objects.get(user_project=ews_project, default=True)
    ews_missions = EwsUserQueries().get_missions(ews_project.ews_name)

    return render(request, "projects/single_project.html", {"ews_missions": ews_missions, "ews_project": ews_project,
                                                            "config_pk": config.pk, "masking_pk": masking.pk})


@login_required
def automatic_mode(request, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    automatic = json.loads(request.GET.get('automatic'))

    if automatic:
        ews_commands.start_automatic_mode(ews_project.ews_name)
    else:
        ews_commands.stop_automatic_mode(ews_project.ews_name)

    ews_project.automatic_mode = automatic
    ews_project.save(update=True)

    return JsonResponse({"automatic": automatic})


@login_required
def project_settings(request, project_pk, config_pk, action=None):
    user_project = UserProject.objects.get(pk=project_pk)
    config = Config.objects.get(pk=config_pk)
    user_configs = Config.objects.filter(user_project=user_project)
    shape_settings_form = ConfigShapeForm(user_project, config)

    if request.method == "GET":
        form = ConfigForm(user_project.sensor.config_name, config.json_configs,
                          initial={"name": config.name, "description": config.description,
                                   "default": config.default})

        upload_form = UploadShapeForm()

        if action == "delete":
            config.delete()
            config = Config.objects.get(default=True)

            return redirect("config-pk", project_pk, config.pk)

        elif action == "reset":
            form = ConfigForm(user_project.sensor.config_name,
                              initial={"name": config.name, "description": config.description,
                                       "default": config.default})

        return render(request, "project/config.html", {"form": form, "project_pk": project_pk,
                                                       "user_configs": user_configs, "config": config,
                                                       "user_project": user_project,
                                                       "upload_form": upload_form,
                                                       "shape_settings_form": shape_settings_form})

    if request.method == "POST":
        upload_form = UploadShapeForm(request.POST, request.FILES)
        user_form = ConfigForm(user_project.sensor.config_name, None, request.POST)
        aoi_form = ConfigShapeForm(user_project, config, request.POST)

        if upload_form.is_valid():
            try:
                tools.handle_shape_upload(upload_form, user_project)
                messages.add_message(request, messages.SUCCESS,
                                     'Shapefile was uploaded successfully!',
                                     extra_tags='alert-success')
            except:
                messages.add_message(request, messages.SUCCESS,
                                     'Shapefile could not be uploaded!'
                                     ' Please check if the zip file contains a shapefile.',
                                     extra_tags='alert-danger')

            return redirect("config-pk", project_pk, config_pk)

        elif user_form.is_valid():
            if aoi_form.is_valid():
                aoi_form_data = aoi_form.cleaned_data
            else:
                aoi_form_data = {"imgpart": None, "mask_image": None, "polygonstatistics": None}

            form_data = user_form.cleaned_data
            name = form_data.pop("name")
            description = form_data.pop("description")

            config_check = Config.objects.filter(name=name)

            if bool(int(request.POST["default"])):
                Config.objects.filter(user_project=user_project).update(default=False)

            if config_check.exists():
                user_config = config_check.first()
                user_config.name = name
                user_config.description = description
                user_config.json_configs = form_data
                user_config.imgpart = get_entry_by_pk(aoi_form_data["imgpart"])
                user_config.mask_image = get_entry_by_pk(aoi_form_data["mask_image"])
                user_config.polygonstatistics = get_entry_by_pk(aoi_form_data["polygonstatistics"])
                if bool(int(request.POST["default"])):
                    user_config.default = True
                user_config.save()

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was updated successfully!',
                                     extra_tags='alert-success')
            else:
                new_config = Config.objects.create(user_project=user_project,
                                                   name=name,
                                                   description=description,
                                                   default=bool(int(request.POST["default"])),
                                                   json_configs=form_data,
                                                   imgpart=get_entry_by_pk(aoi_form_data["imgpart"]),
                                                   mask_image=get_entry_by_pk(aoi_form_data["mask_image"]),
                                                   polygonstatistics=get_entry_by_pk(aoi_form_data["polygonstatistics"])
                                                   )

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was created successfully!',
                                     extra_tags='alert-success')
                config_pk = new_config.pk

            return redirect("config-pk", project_pk, config_pk)


@login_required
def masking_settings(request, project_pk, masking_pk, action=None):
    user_project = UserProject.objects.get(pk=project_pk)
    config = Masking.objects.get(pk=masking_pk)

    if request.method == "GET":
        user_configs = Masking.objects.filter(user_project=user_project)
        form = MaskingForm(config.json_configs,
                           initial={"name": config.name, "description": config.description,
                                    "default": config.default})

        if action == "delete":
            config.delete()
            config = Masking.objects.get(default=True)

            return redirect("config-pk", project_pk, config.pk)

        elif action == "reset":
            form = MaskingForm(
                initial={"name": config.name, "description": config.description,
                         "default": config.default})

        return render(request, "project/masking.html", {"form": form, "project_pk": project_pk,
                                                        "user_configs": user_configs, "config": config,
                                                        "user_project": user_project})

    if request.method == "POST":
        user_form = MaskingForm(None, request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            name = form_data.pop("name")
            description = form_data.pop("description")

            config_check = Masking.objects.filter(name=name)

            if bool(int(request.POST["default"])):
                Masking.objects.filter(user_project=user_project).update(default=False)

            if config_check.exists():
                user_config = config_check.first()
                user_config.name = name
                user_config.description = description
                user_config.json_configs = form_data
                if bool(int(request.POST["default"])):
                    user_config.default = True
                user_config.save()

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was updated successfully!',
                                     extra_tags='alert-success')
            else:
                user_config = Masking.objects.create(user_project=user_project,
                                                     name=name,
                                                     description=description,
                                                     default=bool(int(request.POST["default"])),
                                                     json_configs=form_data)

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was created successfully!',
                                     extra_tags='alert-success')

            user_configs = Masking.objects.filter(user_project=user_project)

            return render(request, "project/masking.html", {"form": user_form, "project_pk": project_pk,
                                                            "user_configs": user_configs, "config": user_config})


@login_required
def download_data_for_project(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    if request.method == "GET":
        sensor_date = user_project.sensor.start_date
        return render(request, "project/download.html", {"project_pk": project_pk, "sensor_date": sensor_date})
    elif request.method == "POST":
        data = json.loads(request.body)

        # EWS Command
        status = ews_commands.prepare_download_selected(user_project.ews_name, data["selected_idents"])

        return JsonResponse({"status": status})


def download_status_for_project(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
    download_queries = DownloadQuery.objects.using("ews").filter(ews_project=ews_project)
    results = {d_query: FileDownload.objects.using("ews").filter(download_query=d_query) for d_query in
               download_queries}

    return render(request, "project/download-status.html", {"user_project": user_project,
                                                            "results": results,
                                                            "project_pk": project_pk})


def download_final_results(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
    final_downloads = Mission.objects.using("ews").filter(ews_project=ews_project)  # TODO , state="finished"
    return render(request, "project/download-results.html", {"project_pk": project_pk, "ews_missions": final_downloads})
