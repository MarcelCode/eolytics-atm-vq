from ews_communication import ews_commands
from missions.models import MissionActionBlock
from django.http import HttpResponse, JsonResponse
from ews_db_connector.models import Mission
import json
import copy

with open(r"templates/mission/mission_options.json") as fo:
    MISSION_OPTIONS = json.load(fo)


def check_mission_block(request):
    data = json.loads(request.body)
    ews_mission_pk = data['ews_mission_pk']
    state = data['ews_state']

    mission_block, created = MissionActionBlock.objects.get_or_create(id=ews_mission_pk)
    mission_options = copy.deepcopy(MISSION_OPTIONS)
    if mission_block.stop_after_block:
        items = mission_options["block_true"][state]
        try:
            items["stop_after_block"]["items"][f"stop_after_{mission_block.block_name}"]["className"] = "bold-menu"
        except:
            pass
    else:
        items = mission_options["block_false"][state]

    return JsonResponse(items)


def handle_mission_block(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ews_mission_pk = data["ews_mission_pk"]
        action = data["action"]
        ews_mission = Mission.objects.using("ews").get(pk=ews_mission_pk)
        block_info, created = MissionActionBlock.objects.get_or_create(pk=ews_mission_pk)

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
            block_info.save()
            print(action)
        elif action == "rerun_block":
            ews_commands.start_job(ews_mission.ews_project.ews_name, ews_mission.ident,
                                   block_name=block_info.block_name, rerun_block=True)
            print(action)

        elif "stop_after" in action:
            stop_block = action.split("_")[-1]
            block_info.stop_after_block = True
            block_info.block_name = stop_block
            block_info.save()

        return HttpResponse(status=200)

    return HttpResponse(status=404)

