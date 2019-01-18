from ews_db_connector import models as ews_models
from projects import models as web_models


class EwsUserQueries(object):

    def __init__(self, user_projects):
        self.ews_numbers = user_projects.values_list("ews_name", flat=True)
        self.ews_project_db_object = ews_models.EwsProject.objects.using("ews")
        self.ews_mission_db_object = ews_models.Mission.objects.using("ews")
        self.user_ews_projects = self.ews_project_db_object.in_bulk(self.ews_numbers, field_name="ews_name")

    def get_states_for_projects(self):
        project_states_dict = {ews_name: self.get_mission_state_single_project(project_object)
                               for ews_name, project_object in self.user_ews_projects.items()}

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
