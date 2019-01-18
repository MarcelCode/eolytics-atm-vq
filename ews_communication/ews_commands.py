
def create_ews_project(project_abbreviation, user_project_name, sensor_id, water_type, region, project, imagepart=None):
    """
    :param project_abbreviation: <string> 3 chars f.e. bra
    :param user_project_name: User project name <string> f.e. Testproject 1.5 (Sensor 1)
    :param sensor_id: Sensor id in db <int>
    :param water_type: Watertype number <int> fe. 4
    :param region: region name f.e. br-lactec, br-project99
    :param project: project name <string>
    :param imagepart: imagepart: <string>; comma sep. geo coords: ul_lat,ul_lon,lr_lat,lr_lon
    :return ews_number: created by ews generator
    """

    print("Create EWS project: ")
    ews_number = "test_00001"

    return ews_number
