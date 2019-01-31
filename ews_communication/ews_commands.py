import requests
import json

URL_RPC_SERVER = "http://172.28.1.250:4691/jsonrpc"
HEADERS = {'content-type': 'application/json'}


def create_ews_project(user_project_name, project_abbrevation, sensor_id, watertype, region, project, imagepart=None):
    """
    :param project_abbrevation: <string> 3 chars f.e. bra
    :param user_project_name: User project name <string> f.e. Testproject 1.5 (Sensor 1)
    :param sensor_id: Sensor id in db <int>
    :param watertype: Watertype number <int> fe. 4
    :param region: region name f.e. br-lactec, br-project99
    :param project: project name <string>
    :param imagepart: imagepart: <string>; comma sep. geo coords: ul_lat,ul_lon,lr_lat,lr_lon
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
            "imagepart": imagepart
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


def updateQueue(ews_name):
    """
    Creates new missions from raw data
    Should be triggered if user presses reload
    """
    payload = {
        "method": "updateOrderQueue",
        "params": {
            "ews_name": ews_name
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()
    return True


def start_automatic_mode(ews_name):
    """
    Sets all running missions to 'interrupted'.
    Starts server.py
    """
    payload = {
        "method": "automaticModeStarted",
        "params": {
            "ews_name": ews_name
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


def download_raw_data(ews_name, sensor_id, ulx, uly, lrx, lry, cloud_cover, start_date, end_date):
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
            "end_date": end_date
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(URL_RPC_SERVER, data=json.dumps(payload), headers=HEADERS).json()

    return True
