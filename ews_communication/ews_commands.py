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
            "region": region,   # br + region
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


def start_job():
    pass


def stop_job():
    pass


def updateQueue():
    pass


def start_automatic_mode():
    pass


def stop_automatic_mode():
    pass


def download_raw_data():
    pass