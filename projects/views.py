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
from sensor_configs.models import Config, Masking, Watertype
from sensor_configs.forms import ConfigForm, MaskingForm, UploadShapeForm, ConfigShapeForm
from sensor_configs import tools
from projects.tools import get_entry_by_pk
from projects.decorators import owns_user_project
from .tools import bytes_to_gb, get_percentage
from collections import OrderedDict
from geodata.models import UserProjectShape
import re


def get_filtered_user_projects(project_states, user_projects, status):
    filtered_projects = [ews_name for ews_name, state in project_states.items() if state == status]
    user_projects = user_projects.filter(ews_name__in=filtered_projects)

    return user_projects


@login_required
def projects(request, status):
    if request.method == "POST":
        user_project_form = forms.CreateProjectForm(request.user, request.POST)

        if user_project_form.is_valid():
            # EWS Command
            watertype = Watertype.objects.first() # Hardcoded first watertype: Standard
            user_info = Profile.objects.get(user=request.user)
            form = user_project_form.cleaned_data
            ews_region = user_info.region_code + re.sub('[^A-Za-z]+', '', form["region"]).lower()
            ews_name = ews_commands.create_ews_project(user_project_name=form['user_project_name'],
                                                       project_abbrevation="atm",
                                                       sensor_id=form['sensor'].ews_id,
                                                       watertype=watertype.ews_id,
                                                       region=ews_region,
                                                       project=user_info.project_name,
                                                       user=user_info.ews_user_id)

            if ews_name:
                cleaned_form = user_project_form.cleaned_data
                cleaned_form["watertype"] = watertype
                cleaned_form["project_abbrevation"] = "atm"
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

    # Cores
    cores = Profile.objects.get(user=request.user).cpu_cores
    cores = list(range(1, cores + 1))
    ews_queries = ews_requests.EwsUserQueries()
    project_states = ews_queries.get_states_for_projects(user_projects)
    state_count = Counter(project_states.values())
    state_count["all"] = len(user_projects)

    if status in ["running", "failed", "running_failed"]:
        user_projects = get_filtered_user_projects(project_states, user_projects, status)

    # temporarily add states to projects
    for project_object in user_projects:
        project_object.state = project_states[project_object.ews_name]

    return render(request, "projects/projects.html", {"status": status,
                                                      "project_states": project_states, "table": user_projects,
                                                      "state_count": state_count, "cores": cores, })


@login_required
@owns_user_project
def delete_project(request, status, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    ews_commands.remove_ews_project(ews_project.ews_name)

    ews_project.delete()

    return redirect("projects", status)


@login_required
@owns_user_project
def project(request, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    config = Config.objects.get(user_project=ews_project, default=True)
    masking = Masking.objects.get(user_project=ews_project, default=True)
    states = ["finished", "empty", "failed"]

    return render(request, "projects/single_project.html", {"ews_project": ews_project,
                                                            "config_pk": config.pk,
                                                            "masking_pk": masking.pk,
                                                            "states": states})


@login_required
@owns_user_project
def automatic_mode(request, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    automatic = json.loads(request.GET.get('automatic'))

    if automatic:
        core_usage = EwsUserQueries().get_core_usage(request.user, ews_project.ews_name)
        available_cores = Profile.objects.get(user=request.user).cpu_cores
        rest_cores = available_cores - core_usage
        if ews_project.cores > rest_cores:
            return JsonResponse({"status": False})
        else:
            ews_commands.start_automatic_mode(ews_project.ews_name, cores=ews_project.cores)
    else:
        ews_commands.stop_automatic_mode(ews_project.ews_name)

    ews_project_query = UserProject.objects.filter(pk=project_pk)
    ews_project_query.update(automatic_mode=automatic)

    return JsonResponse({"automatic": automatic})


@login_required
@owns_user_project
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
                aoi_form_data = {"aoi": None}

            form_data = user_form.cleaned_data
            name = form_data.pop("name")
            description = form_data.pop("description")

            config_check = Config.objects.filter(user_project=user_project, name=name)

            if bool(int(request.POST["default"])):
                Config.objects.filter(user_project=user_project).update(default=False)

            if config_check.exists():
                user_config = config_check.first()
                user_config.name = name
                user_config.description = description
                user_config.json_configs = form_data
                user_config.aoi = get_entry_by_pk(aoi_form_data["aoi"], UserProjectShape)
                if bool(int(request.POST["default"])):
                    user_config.default = True
                user_config.save()

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was updated successfully!',
                                     extra_tags='alert-success')
            else:
                user_config = Config.objects.create(user_project=user_project,
                                                    name=name,
                                                    description=description,
                                                    default=bool(int(request.POST["default"])),
                                                    json_configs=form_data,
                                                    aoi=get_entry_by_pk(aoi_form_data["aoi"], UserProjectShape),
                                                    )

                messages.add_message(request, messages.SUCCESS,
                                     f'Configuration {name} was created successfully!',
                                     extra_tags='alert-success')

            if user_config.default:
                json_config = tools.serialize_config_model(user_config)
                ews_commands.set_global_job_settings(user_project.ews_name, json_config)

            return redirect("config-pk", project_pk, config_pk)

        else:
            return render(request, "project/config.html", {"form": user_form, "project_pk": project_pk,
                                                           "user_configs": user_configs, "config": config,
                                                           "user_project": user_project,
                                                           "upload_form": upload_form,
                                                           "shape_settings_form": aoi_form})


@login_required
@owns_user_project
def masking_settings(request, project_pk, masking_pk, action=None):
    user_project = UserProject.objects.get(pk=project_pk)
    config = Masking.objects.get(pk=masking_pk)

    if request.method == "GET":
        user_configs = Masking.objects.filter(user_project=user_project)
        form = MaskingForm(user_project.sensor.config_name, config.json_configs,
                           initial={"name": config.name, "description": config.description,
                                    "default": config.default})

        if action == "delete":
            config.delete()
            config = Masking.objects.get(default=True)

            return redirect("config-pk", project_pk, config.pk)

        elif action == "reset":
            form = MaskingForm(user_project.sensor.config_name,
                               initial={"name": config.name, "description": config.description,
                                        "default": config.default})

        return render(request, "project/masking.html", {"form": form, "project_pk": project_pk,
                                                        "user_configs": user_configs, "config": config,
                                                        "user_project": user_project})

    if request.method == "POST":
        user_form = MaskingForm(user_project.sensor.config_name, None, request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            name = form_data.pop("name")
            description = form_data.pop("description")

            config_check = Masking.objects.filter(user_project=user_project, name=name)

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

            if bool(int(request.POST["default"])):
                ews_commands.set_global_mask_definitions(user_project.ews_name, user_config.json_configs)

            return render(request, "project/masking.html", {"form": user_form, "project_pk": project_pk,
                                                            "user_configs": user_configs, "config": user_config})


@login_required
@owns_user_project
def download_data_for_project(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    if request.method == "GET":
        upload_form = UploadShapeForm()
        user_shapes = UserProjectShape.objects.filter(user_project=user_project)
        sensor_date = user_project.sensor.start_date
        return render(request, "project/download.html", {"project_pk": project_pk, "sensor_date": sensor_date,
                                                         "user_shapes": user_shapes,
                                                         "upload_form": upload_form})
    elif request.method == "POST":
        data = json.loads(request.body)

        # EWS Command
        status = ews_commands.prepare_download_selected(user_project.ews_name, data["selected_idents"])

        return JsonResponse({"status": status})


@login_required
@owns_user_project
def download_status_for_project(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)

    return render(request, "project/download-status.html", {"user_project": user_project,
                                                            "project_pk": project_pk})


@login_required
@owns_user_project
def download_status_single(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
    download_queries = DownloadQuery.objects.using("ews").filter(ews_project=ews_project, auto_harvest=False)\
        .order_by('-creation_datetime')
    results = {d_query: FileDownload.objects.using("ews").filter(download_query=d_query) for d_query in
               download_queries}

    return render(request, "project/download-status-single.html", {"user_project": user_project,
                                                                   "results": results,
                                                                   "project_pk": project_pk})


@login_required
@owns_user_project
def download_status_continuous(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
    download_queries = DownloadQuery.objects.using("ews").filter(ews_project=ews_project, auto_harvest=True) \
        .order_by('-creation_datetime')
    results = {d_query: FileDownload.objects.using("ews").filter(download_query=d_query) for d_query in
               download_queries}

    return render(request, "project/download-status-continuous.html", {"user_project": user_project,
                                                                       "results": results,
                                                                       "project_pk": project_pk})


@login_required
@owns_user_project
def download_final_results(request, project_pk):
    user_project = UserProject.objects.get(pk=project_pk)
    ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
    final_downloads = Mission.objects.using("ews").filter(ews_project=ews_project, state="finished")
    return render(request, "project/download-results.html", {"project_pk": project_pk, "ews_missions": final_downloads})


@login_required
def create_project(request):
    create_project_form = forms.CreateProjectForm(user=request.user)

    return render(request, "projects/create_project_modal.html", {"form": create_project_form})


@login_required
def get_memory_info(request):
    user = request.user
    ews_user_id = Profile.objects.get(user=user).ews_user_id

    memory_dict = ews_commands.get_free_space_by_user(user=str(ews_user_id))
    memory_space = bytes_to_gb(memory_dict.pop("total_space"))
    free_space = bytes_to_gb(memory_dict.pop("free_space"))
    space_left_percent = get_percentage(memory_space, free_space)
    memory_dict = {UserProject.objects.get(ews_name=key).user_project_name:
                       [bytes_to_gb(value), get_percentage(memory_space, bytes_to_gb(value))]
                   for key, value in memory_dict.items()}

    memory_dict = OrderedDict(sorted(memory_dict.items()))

    return render(request, "projects/memory_info_modal.html", {"memory_dict": memory_dict,
                                                               "memory_space": memory_space,
                                                               "free_space": free_space,
                                                               "space_left_percent": space_left_percent})


@login_required
def change_project_cores(request):
    data = json.loads(request.body)
    user_projects = UserProject.objects.filter(pk=data["project_pk"])
    user_project = user_projects.first()
    if user_project.user == request.user:
        if user_project.automatic_mode:
            ews_commands.automatic_mode_cores_changed(data["ews_name"], int(data["cores"]))
        else:
            running_missions = Mission.objects.using("ews").filter(ews_project__ews_name=data["ews_name"], state="running")

            if len(running_missions) > int(data["cores"]):
                return JsonResponse({"status": False})

        user_projects.update(cores=data["cores"])

        return JsonResponse({"status": True})

    return HttpResponse(status=401)


@login_required
@owns_user_project
def download_cancel(request, project_pk):
    if request.method == "POST":
        data = json.loads(request.body)
        ews_commands.cancel_raw_download(data["download_query_id"])

    return JsonResponse({"status": True})


@login_required
@owns_user_project
def download_cancel_continuous(request, project_pk):
    if request.method == "POST":
        data = json.loads(request.body)
        ews_commands.cancel_auto_raw_download(data["download_query_id"])

    return JsonResponse({"status": True})


@login_required
def reset_mission_by_state(request):
    data = json.loads(request.body)
    project_pk = data["project_pk"]
    entry = UserProject.objects.get(pk=project_pk)
    if entry.user == request.user:
        ews_commands.reset_all_by_state(data["ews_name"], data["state"])

        return JsonResponse({"status": True})

    return JsonResponse({"status": False})


def upload_aoi_download(request, project_pk):
    if request.method == "POST":
        user_project = UserProject.objects.get(pk=project_pk)
        upload_form = UploadShapeForm(request.POST, request.FILES)

        if upload_form.is_valid():
            try:
                tools.handle_shape_upload(upload_form, user_project)
                messages.add_message(request, messages.SUCCESS,
                                     'Shapefile was uploaded successfully!',
                                     extra_tags='alert-success')
            except ValueError as e:
                if e.args[1] == 1:
                    messages.add_message(request, messages.SUCCESS, str(e.args[0]),
                                         extra_tags='alert-info')
                elif e.args[1] == 2:
                    messages.add_message(request, messages.SUCCESS, str(e.args[0]),
                                         extra_tags='alert-danger')

            except Exception as e:
                messages.add_message(request, messages.SUCCESS,
                                     'Shapefile could not be uploaded!'
                                     ' Please check if the zip file contains a shapefile.',
                                     extra_tags='alert-danger')

            return redirect("project-download", project_pk)