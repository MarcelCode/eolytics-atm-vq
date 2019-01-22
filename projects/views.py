from django.shortcuts import render, redirect
from .forms import CreateProjectForm
from .models import UserProject
from ews_db_connector.ews_requests import EwsUserQueries
from accounts.models import Profile
from ews_communication import ews_commands
from ews_db_connector import ews_requests
from collections import Counter
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def get_filtered_user_projects(project_states, user_projects, status):
    filtered_projects = [ews_name for ews_name, state in project_states.items() if state == status]
    user_projects = user_projects.filter(ews_name__in=filtered_projects)

    return user_projects


@login_required
def projects(request, status):
    create_project_form = CreateProjectForm(user=request.user)
    if request.method == "POST":
        user_project_form = CreateProjectForm(request.user, request.POST)
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
    ews_missions = EwsUserQueries().get_missions(ews_project.ews_name)

    return render(request, "projects/single_project.html", {"ews_missions": ews_missions, "ews_project": ews_project})


@login_required
def automatic_mode(request, project_pk):
    ews_project = UserProject.objects.get(pk=project_pk)
    automatic = json.loads(request.GET.get('automatic'))

    if automatic:
        ews_commands.start_automatic_mode()
    else:
        ews_commands.stop_automatic_mode()

    ews_project.automatic_mode = automatic
    ews_project.save()

    return JsonResponse({"automatic": automatic})
