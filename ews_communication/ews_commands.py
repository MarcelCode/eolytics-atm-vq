import requests
import json
import os
from decouple import config

# URL_RPC_SERVER = "http://192.168.254.10:4691/jsonrpc"
ews_ip = config("EWS_HOST")
URL_RPC_SERVER = f"http://{ews_ip}:4691/jsonrpc"
HEADERS = {'content-type': 'application/json'}


def create_ews_project(user_project_name, project_abbrevation, sensor_id, watertype, region, project, imagepart=None,
                       user='20030'):
    """
    :param project_abbrevation: <string> 3 chars f.e. bra
    :param user_project_name: User project name <string> f.e. Testproject 1.5 (Sensor 1)
    :param sensor_id: Sensor id in db <int>
    :param watertype: Watertype number <int> fe. 4
    :param region: region name f.e. br-lactec, br-project99
    :param project: project name <string>
    :param imagepart: imagepart: <string>; comma sep. geo coords: ul_lat,ul_lon,lr_lat,lr_lon
    :param user: wird manuell vergeben und entspricht dem Ordner auf dem SFTP
    :return ews_number: created by ews generator e.g. EWS00001
    """
    payload = {
        "method": "createNewProject",
        "params": {
            "project_abbreviation": project_abbrevation,
            "user_project_name": user_project_name,
            "sensor_id": sensor_id,
            "water_type": watertype,
            "project": project,
            "region": region,  # br + region
            "imagepart": imagepart,
            "user": user
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    try:
        ews_name = response["result"]
    except KeyError:
        ews_name = False
        print(response['error'])
    return ews_name


def remove_ews_project(ews_name):
    print(f"delete project: {ews_name}")
    payload = {
        "method": "removeProject",
        "params": {
            "ews_name": ews_name
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def start_job(ews_name, mission_ident, begin_action=0, block_name=None, rerun_block=False):
    """
    First start: begin_action 0 or 1
    Continue: begin_action 0, 0 means last failed/stopped action
    Restart: begin_action 1
    :param ews_name: e.g. EWS00001
    :param mission_ident: e.g. bra180718ls8.132117
    :param begin_action: e.g. 0
    :param block_name:  defined blockname or None
    :param rerun_block: True or False
    :return:
    """
    payload = {
        "method": "startJob",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident,
            "begin_action": begin_action,
            "block_name": block_name,
            "rerun_block": rerun_block
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def stop_job(ews_name, mission_ident):
    """
    kills job process
    sets mission to state 'stopped'
    :param ews_name: e.g. EWS00001
    :param mission_ident: e.g. bra180718ls8.132117
    :return:
    """
    payload = {
        "method": "stopJob",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def start_automatic_mode(ews_name, use_local_settings=False, cores=2):
    """

    :param ews_name:
    :param use_local_settings:
    :param cores:
    :return:
    """
    payload = {
        "method": "automaticModeStarted",
        "params": {
            "ews_name": ews_name,
            "use_local_settings": use_local_settings,
            "cores": cores,

        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def stop_automatic_mode(ews_name):
    """
    Terminates server.py process
    Sets all running missions to stopped
    """
    payload = {
        "method": "automaticModeTerminated",
        "params": {
            "ews_name": ews_name
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def download_raw_data(ews_name, sensor_id, ulx, uly, lrx, lry, cloud_cover, start_date, end_date, future_download=False):
    """
    :param ews_name: EWS name
    :param sensor_id: Sensor id
    :param ulx: upper left x (which coordinate system??)
    :param uly: upper left y
    :param lrx: lower right x
    :param lry: lower right y
    :param cloud_cover: floating point [0.0, 100.0]
    :param start_date: string YYYYMMDD
    :param end_date: string YYYYMMDD
    :return:
    """
    payload = {
        "method": "downloadSatelliteRawdata",
        "params": {
            "ews_name": ews_name,
            "sensor_id": sensor_id,
            "ulx": ulx,
            "uly": uly,
            "lrx": lrx,
            "lry": lry,
            "cloud_cover": int(cloud_cover),
            "start_date": start_date,
            "end_date": end_date,
            "is_future": future_download
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()

    return True


def cancel_raw_download(download_query_id):
    """

    :param download_query_id: Query for get the scenes
    :return:
    """

    payload = {
        "method": "cancelSatelliteRawdataDownload",
        "params": {
            "download_query_id": download_query_id
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()

    return True


def cancel_auto_raw_download(download_query_id):
    """
    :param download_query_id: Query for get the scenes
    :return:
    """

    payload = {
        "method": "cancelAutoRawdataDownload",
        "params": {
            "download_query_id": download_query_id
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def reset_all_by_state(ews_name, state):
    """

    :param ews_name: e.g. EWS0001
    :param state: e.g. finished
    :return: True
    """

    payload = {
        "method": "resetAllByState",  # TODO Moritz method!
        "params": {
            "ews_name": ews_name,
            "state": state
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()

    return True


def set_local_job_settings(ews_name, json_configuration, mission_ident):
    """
    Sets local job settings: job_settings.json
    :param ews_name: e.g. EWS0001
    :param json_configuration: e.g. {"product_list":["abs", "aot", ...], "scaled_workflow":false, ...}
    :param mission_ident: e.g. bra180718ls8.132117
    :return: True
    """
    payload = {
        "method": "setLocalJobSettings",
        "params": {
            "ews_name": ews_name,
            "json_configuration": json_configuration,
            "order_ident": mission_ident
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    print("set_local_job_settings")
    return True


def reset_local_job_settings(ews_name, mission_ident):
    """

    :param ews_name: e.g. EWS0001
    :param mission_ident: e.g. bra180718ls8.132117
    :return:
    """

    payload = {
        "method": "resetLocalJobSettings",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    print("reset_local_job_settings")
    return True


def set_global_job_settings(ews_name, json_configuration):
    payload = {
        "method": "setGlobalJobSettings",
        "params": {
            "ews_name": ews_name,
            "json_configuration": json_configuration,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def set_local_mask_definitions(ews_name, json_configuration, mission_ident):
    """
    Sets local mask_definitions.cfg
    :param ews_name: e.g. EWS0001
    :param json_configuration: e.g. {"blue_treshold": 0.4, "cloud_ir_treshold": ...}
    :param mission_ident: e.g. bra180718ls8.132117
    :return:
    """
    payload = {
        "method": "setLocalMaskDefinitions",
        "params": {
            "ews_name": ews_name,
            "json_configuration": json_configuration,
            "order_ident": mission_ident
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    print("set_local_mask_definitions")
    return True


def reset_local_mask_definitions(ews_name, mission_ident):
    """
    Resets local mask_definitions.cfg
    :param ews_name: e.g. EWS0001
    :param mission_ident: e.g. bra180718ls8.132117
    :return:
    """
    payload = {
        "method": "resetLocalMaskDefinitions",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    print("reset_local_mask_definitions")
    return True


def set_global_mask_definitions(ews_name, json_configuration):
    payload = {
        "method": "setGlobalMaskDefinitions",
        "params": {
            "ews_name": ews_name,
            "json_configuration": json_configuration,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def continue_job_in_automatic_mode(ews_name, mission_ident):
    """
    Sets stopped job to "interrupted". Job will be started with action = last_action
    in automatic mode when a core is free.
    """
    payload = {
        "method": "reactivateJobInAutomaticMode",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def reset_job_in_automatic_mode(ews_name, mission_ident):
    """
    Sets stopped job to "new" and action_nb to 0.
    """
    payload = {
        "method": "resetJobInAutomaticMode",
        "params": {
            "ews_name": ews_name,
            "order_ident": mission_ident,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def prepare_download_selected(ews_name, ews_ident_list):
    """
    :param ews_name: EWS Name
    :param ews_ident_list: List of selected Missions --> ews_ident
    :return: status --> True (download will be prepared), False (memory full)
    """
    payload = {
        "method": "uploadResults",
        "params": {
            "ews_name": ews_name,
            "order_idents_list": ews_ident_list,
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    try:
        has_enough_memory_left = response["result"]
    except KeyError:
        has_enough_memory_left = True
        print(response['error'])
    return has_enough_memory_left


def get_free_space_by_user(user='20030'):
    """
    :param user: User id, defined in model Profile
    :return: dict with space memory, free space memory and free space memory per ews_name
    """

    payload = {
        "method": "getDataDiskSpaceByUser",
        "params": {
            "user": str(user),
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    try:
        memory_dict = response["result"]
    except KeyError:
        memory_dict = None
        print(response['error'])

    return memory_dict
