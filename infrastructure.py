from config.config_manager import ConfigManager
from config.manage_json_config import get_dict_value
from local import setup_database as Database
from local.artifacts.manage_artifacts import ManageArtifacts
from util import file_actions as File
from website.api.teamcity import TeamCity

config_file_path = r'config/json_config/config_path.json'
configuration = ConfigManager(path_to_master_config=config_file_path)

teamcity_handler = TeamCity


def check_teamcity_available():
    teamcity_setting = configuration.get_teamcity()
    if teamcity_setting:
        global teamcity_handler
        teamcity_handler = TeamCity(host=get_dict_value(teamcity_setting, ["host"]),
                                    username=get_dict_value(teamcity_setting, ["teamcity_username"]),
                                    password=get_dict_value(teamcity_setting, ["teamcity_password"]))
        response = teamcity_handler.get_url_response(url=get_dict_value(teamcity_setting, ["host"]))
        if response:
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print "Incorrect TeamCity login credentials"
                return False
        else:
            print "Cannot reach TeamCity"
            return False


def check_database_connection():
    database_setting = configuration.get_database()
    if database_setting:
        database = Database.get_database_connection(server=get_dict_value(database_setting, ["db_server"]),
                                                    username=get_dict_value(database_setting, ["db_username"]),
                                                    password=get_dict_value(database_setting, ["db_password"]))
        if database.connection:
            return True
    else:
        return False


def start_controller_setup(test_mode):
    pass


def controller_infrastructure_ready():
    status = True

    if configuration.get_load_status():
        print "Configuration files: Ok"
    else:
        print "Configuration files: Fail"
        print "Could not load: {}".format(str(configuration.get_list_of_failed_configs())[1:-1])

    if check_teamcity_available():
        print "TeamCity server: Ok"
    else:
        print "TeamCity server: Bad"
        return False
    if check_database_connection():
        print "Database server: Ok"
    else:
        print "Database server: Bad"
        return False
    return status


def start_controller_setup(test_mode):
    artifact = ManageArtifacts()

    # Download all artifacts
    artifact.download_artifacts()

    # Replace old with new artifacts

    artifact.replace_artifacts()


    sql_path = os.path.join(deployment_env_paths["path_download_root"], local_database_setting["db_to_setup"])

    if File.file_exists(sql_path):
        Database.recreate_database_from_script(sql_path)


