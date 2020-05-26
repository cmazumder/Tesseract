from DeployementLog import DeploymentLog
from config.config_manager import ConfigManager
from config.manage_json_config import get_dict_value
from local import database_setup as Database
from local.artifacts.download_application import DownloadApplication
from local.artifacts.manage_artifacts import ManageApplication
from util import folder_actions as Folder
from website.api.teamcity import TeamCity


class Infrastructure:

    def __init__(self):
        self.ConfigurationManager = ConfigManager.get_instance()
        self.application_setting = self.ConfigurationManager.get_artifacts_to_download()
        self.teamcity_setting = self.ConfigurationManager.get_teamcity()
        self.database_setting = self.ConfigurationManager.get_database()
        self.environment_setting = self.ConfigurationManager.get_environment_setting()

    def check_teamcity_available(self):
        teamcity_connection = TeamCity(host=get_dict_value(self.teamcity_setting, ["host"]),
                                       username=get_dict_value(self.teamcity_setting, ["teamcity_username"]),
                                       password=get_dict_value(self.teamcity_setting, ["teamcity_password"]))
        if teamcity_connection:
            response = teamcity_connection.get_teamcity_response()  # type: response
            if response:
                if response.status_code == 200:
                    return True
                elif response.status_code == 401:
                    print "Incorrect TeamCity login credentials | url: {}".format(get_dict_value(self.teamcity_setting, ["host"]))
                    return False
                else:
                    print "Cannot reach TeamCityConnection"
                    return False
        else:
            print "No response | Issue with TeamCity while creating TeamCity connection :{}".format(teamcity_connection)
            return False

    def get_database_connection(self):
        database_connection = Database.get_database_connection(
            server=get_dict_value(self.database_setting, ["db_server"]),
            username=get_dict_value(self.database_setting, ["db_username"]),
            password=get_dict_value(self.database_setting, ["db_password"]))
        if database_connection.connection:
            return database_connection
        else:
            return False

    def check_download_location_ready(self):
        download_location = get_dict_value(self.environment_setting, ["download_artifact_root_path"])
        copy_all_config_location = Folder.build_path(download_location,
                                                     get_dict_value(self.environment_setting, ["artifact_config_folder"]))

        if Folder.create_folder(download_location) and Folder.create_folder(copy_all_config_location):
            return True
        else:
            return False

    def is_ready(self):
        print "Configuration files: Ok"
        if self.check_teamcity_available():
            print "TeamCity server: Ok"
        else:
            print "TeamCity server: Error"
            return False

        if self.check_download_location_ready():
            print "Download location: Ok"
        else:
            print "Download location: Error"
            return False

        if self.get_database_connection():
            print "Database server: Ok"
        else:
            print "Database server: Error"
            return False
        return True

    def get_sql_script(self, app_details):
        # check if sql data is available
        download_handler = get_dict_value(app_details, ["sql", "Download"])  # type: DownloadApplication
        if download_handler and download_handler.get_download_status():
            sql_path = Folder.build_path(download_handler.download_path,
                                         get_dict_value(self.environment_setting, ["db_property", "db_script"]))
            return sql_path
        return None

    def start_setup(self):
        logger = DeploymentLog(get_dict_value(self.environment_setting, ["download_artifact_root_path"]))

        total_database_time = None

        artifact = ManageApplication(app_setting=self.application_setting, env_setting=self.environment_setting)

        # DownloadApplication all artifacts
        start_time = logger.time_it()
        artifact.download_application()
        total_download_time = logger.total_time(start=start_time, end=logger.time_it())

        # Replace old with new artifacts
        start_time = logger.time_it()
        artifact.replace_application()
        total_replace_time = logger.total_time(start=start_time, end=logger.time_it())

        application_details = artifact.get_application_details()  # type: dict

        sql_path = self.get_sql_script(app_details=application_details)

        if sql_path:
            start_time = logger.time_it()
            Database.recreate_database_from_script(database_connection=self.get_database_connection(), sql_path=sql_path,
                                                   delete_db=get_dict_value(self.environment_setting,
                                                                            ["db_property", "db_to_delete"]))

            total_database_time = logger.total_time(start=start_time, end=logger.time_it())


        logger.write_deployment_status(app_details=application_details)
        logger.write_time(time_download=total_download_time, time_replace=total_replace_time,
                          time_db=total_database_time)
