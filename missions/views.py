from ews_communication import ews_commands
from missions.models import MissionActionBlock
from django.http import HttpResponse, JsonResponse
from ews_db_connector.models import Mission
import json
import copy
from missions.tools import MissionMenuPoints, SetMissionSettings, check_core_usage
from django.contrib.auth.decorators import login_required
from projects.models import UserProject


with open(r"templates/mission/mission_options.json") as fo:
    MISSION_OPTIONS = json.load(fo)


@login_required
def check_mission_block(request):
    data = json.loads(request.body)
    ews_mission_pk = data['ews_mission_pk']
    state = Mission.objects.using("ews").get(pk=ews_mission_pk).state
    project_pk = data["project_pk"]
    ews_mode = data["ews_mode"]
    mission_options = copy.deepcopy(MISSION_OPTIONS)

    if not ews_mode:
        mission_block, created = MissionActionBlock.objects.get_or_create(id=ews_mission_pk)

        # Stop Block menu integration
        if mission_block.stop_after_block:
            items = mission_options["block_true"][state]
            try:
                items["stop_after_block"]["items"][f"stop_after_{mission_block.block_name}"]["className"] = "bold-menu"
            except:
                pass
        else:
            items = mission_options["block_false"][state]

        # Remove glint correction sentinel 3
        if UserProject.objects.get(pk=project_pk).sensor.ews_id == 67:
            del items["stop_after_block"]["items"]["stop_after_3"]

        # Config Menus
        if state != "running":
            mission_menu = MissionMenuPoints(items, project_pk)
            items = mission_menu.add_menus()

            if mission_block.config:
                items["workflow_setting"]["items"][f"workflow_{mission_block.config.pk}"]["className"] = "bold-menu"
            if mission_block.masking:
                items["masking_setting"]["items"][f"masking_{mission_block.masking.pk}"]["className"] = "bold-menu"
    else:
        items = mission_options["automatic"][state]

    return JsonResponse(items)


@login_required
def handle_mission_block(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ews_mission_pk = data["ews_mission_pk"]
        action = data["action"]
        ews_mission = Mission.objects.using("ews").get(pk=ews_mission_pk)
        block_info, created = MissionActionBlock.objects.get_or_create(pk=ews_mission_pk)

        if action in ["start", "continue", "restart"]:
            check, message = check_core_usage(request.user)
            print(message)  # TODO delete
            if not check:
                return JsonResponse({"status": False, "message": message})

        if action == "start":
            ews_commands.start_job(ews_mission.ews_project.ews_name, ews_mission.ident, block_name=block_info.block_name)
            print(action)
        elif action == "continue":
            ews_commands.start_job(ews_mission.ews_project.ews_name, ews_mission.ident, block_name=block_info.block_name)
            print(action)
        elif action == "restart":
            ews_commands.start_job(ews_mission.ews_project.ews_name, ews_mission.ident,
                                   block_name=block_info.block_name, begin_action=1)
            print(action)
        elif action == "stop":
            ews_commands.stop_job(ews_mission.ews_project.ews_name, ews_mission.ident)
            print(action)
        elif action == "remove_stop":
            block_info.stop_after_block = False
            block_info.block_name = None
            block_info.save(update_fields=("stop_after_block", "block_name"))
            print(action)
        elif action == "rerun_block":
            ews_commands.start_job(ews_mission.ews_project.ews_name, ews_mission.ident,
                                   block_name=block_info.block_name, rerun_block=True)
            print(action)

        elif action == "automatic_reset":
            ews_commands.reset_job_in_automatic_mode(ews_mission.ews_project.ews_name, ews_mission.ident)

        elif action == "automatic_continue":
            ews_commands.continue_job_in_automatic_mode(ews_mission.ews_project.ews_name, ews_mission.ident)

        elif "stop_after" in action:
            stop_block = action.split("_")[-1]
            block_info.stop_after_block = True
            block_info.block_name = stop_block
            block_info.save(update_fields=("stop_after_block", "block_name"))

        elif "masking" in action or "workflow" in action:
            SetMissionSettings(action, block_info, ews_mission).save_config()

        return HttpResponse(status=200)

    return HttpResponse(status=404)

