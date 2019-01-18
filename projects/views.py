from django.shortcuts import render
from .forms import CreateProjectForm
from .models import UserProject
from ews_communication import ews_commands
from ews_db_connector import ews_requests
from collections import Counter


def get_filtered_user_projects(project_states, user_projects, status):
    filtered_projects = [ews_name for ews_name, state in project_states.items() if state == status]
    user_projects = user_projects.filter(ews_name__in=filtered_projects)

    return user_projects


def projects(request, status):
    create_project_form = CreateProjectForm(user=request.user)
    if request.method == "POST":
        user_project_form = CreateProjectForm(request.user, request.POST)
        if user_project_form.is_valid():
            cleaned_form = user_project_form.cleaned_data
            user_project = UserProject(user=request.user, **cleaned_form)
            user_project.save()

            # EWS Command
            # ews_status = ews_commands.create_ews_project(**user_project_form.cleaned_data)
            # if ews_status:
            #     user_project.save()

    user_projects = UserProject.objects.filter(user=request.user)
    ews_queries = ews_requests.EwsUserQueries(user_projects)
    project_states = ews_queries.get_states_for_projects()
    state_count = Counter(project_states.values())
    state_count["all"] = len(user_projects)

    if status == "running" or status == "failed":
        user_projects = get_filtered_user_projects(project_states, user_projects, status)

    return render(request, "projects/projects.html", {"form": create_project_form, "status": status,
                                                      "project_states": project_states, "table": user_projects,
                                                      "state_count": state_count})
