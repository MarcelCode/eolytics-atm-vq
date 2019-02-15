from ews_db_connector import models as ews_models
from projects.models import UserProject


class EwsUserQueries(object):

    def __init__(self):
        self.ews_project_db_object = ews_models.EwsProject.objects.using("ews")
        self.ews_mission_db_object = ews_models.Mission.objects.using("ews")

    def get_ews_project(self, ews_name):
        ews_project = self.ews_project_db_object.get(ews_name=ews_name)
        return ews_project

    def get_states_for_projects(self, user_projects):
        ews_numbers = user_projects.values_list("ews_name", flat=True)
        user_ews_projects = self.ews_project_db_object.in_bulk(ews_numbers, field_name="ews_name")

        project_states_dict = {ews_name: self.get_mission_state_single_project(project_object)
                               for ews_name, project_object in user_ews_projects.items()}

        return project_states_dict

    def get_mission_state_single_project(self, project):
        mission_states = self.ews_mission_db_object.filter(ews_project=project).values_list("state", flat=True)

        if "failed" in mission_states:
            project_status = "failed"
        elif "running" in mission_states:
            project_status = "running"
        else:
            project_status = "idle"

        return project_status

    def get_missions(self, ews_name):
        ews_project = self.get_ews_project(ews_name)
        missions = self.ews_mission_db_object.filter(ews_project=ews_project)

        return missions

    def get_core_usage(self, user, exclude_ews_name=None):
        user_project_ews_names = list(UserProject.objects.filter(user=user).values_list("ews_name", flat=True))
        if exclude_ews_name:
            if exclude_ews_name in user_project_ews_names:
                user_project_ews_names.remove(exclude_ews_name)
        ews_projects = self.ews_project_db_object.filter(ews_name__in=user_project_ews_names)
        user_missions = self.ews_mission_db_object.filter(ews_project__in=ews_projects)
        cores_in_usage = list(user_missions.values_list("state", flat=True)).count("running")

        return cores_in_usage