from sensor_configs.models import Masking, Config
from projects.models import UserProject
from ews_communication import ews_commands
from sensor_configs.tools import serialize_config_model
from accounts.models import Profile
from ews_db_connector.ews_requests import EwsUserQueries


class MissionMenuPoints(object):

    def __init__(self, items, project_pk):
        self.items = items
        self.user_project = UserProject.objects.get(pk=project_pk)

    def add_workflow_menu(self):
        configs = Config.objects.filter(user_project=self.user_project)
        config_items = {f"workflow_{pk}": {"name": name} for pk, name in configs.values_list("pk", "name")}
        config_items["workflow_reset"] = {"name": "Reset Workflow"}
        self.items["workflow_setting"]["items"] = config_items

        return config_items

    def add_masking_menu(self):
        masking = Masking.objects.filter(user_project=self.user_project)
        config_items = {f"masking_{pk}": {"name": name} for pk, name in masking.values_list("pk", "name")}
        config_items["masking_reset"] = {"name": "Reset Masking"}
        self.items["masking_setting"]["items"] = config_items

        return config_items

    def add_menus(self):
        self.add_workflow_menu()
        self.add_masking_menu()

        return self.items


class SetMissionSettings(object):

    def __init__(self, action, block_info, ews_mission):
        self.action = action
        self.block_info = block_info
        self.action_type = self.action.split("_")[-1]
        self.ews_mission = ews_mission

    def save_config(self):
        if "masking" in self.action:
            if self.action_type == "reset":
                if self.block_info.masking is not None:
                    self.block_info.masking = None
                    self.block_info.save(update_fields=("masking",))

                    ews_commands.reset_local_mask_definitions(self.ews_mission.ews_project.ews_name,
                                                              self.ews_mission.ident)
            else:
                masking_pk = int(self.action_type)
                self.block_info.masking = Masking.objects.get(pk=masking_pk)
                self.block_info.save(update_fields=("masking",))

                ews_commands.set_local_mask_definitions(self.ews_mission.ews_project.ews_name,
                                                        self.block_info.masking.json_configs,
                                                        self.ews_mission.ident)

        elif "workflow" in self.action:
            if self.action_type == "reset":
                if self.block_info.config is not None:
                    self.block_info.config = None
                    self.block_info.save(update_fields=("config",))

                    ews_commands.reset_local_job_settings(self.ews_mission.ews_project.ews_name,
                                                          self.ews_mission.ident)

            else:
                workflow_pk = int(self.action_type)
                self.block_info.config = Config.objects.get(pk=workflow_pk)
                self.block_info.save(update_fields=("config",))

                json = serialize_config_model(self.block_info.config)
                ews_commands.set_local_job_settings(self.ews_mission.ews_project.ews_name,
                                                    json,
                                                    self.ews_mission.ident)

        return self.block_info


def check_core_usage(user):
    allowed_cores = Profile.objects.get(user=user).cpu_cores
    cores_in_usage = EwsUserQueries().get_core_usage(user)

    usage_string = f"{cores_in_usage} of {allowed_cores} cores in usage."

    if allowed_cores > cores_in_usage:
        return True, usage_string
    else:
        return False, usage_string
