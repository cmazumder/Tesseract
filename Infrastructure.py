from DeploymentLog import DeploymentLog
from config.config_manager import ConfigManager
from config.manage_json_config import get_dict_value
from local.DatabaseSetup import DatabaseSetup as Database
from local.ManageApplicationDownload import ManageApplicationDownload
from local.ManageApplicationReplace import ManageApplicationReplace
from local.ManagePostDownload import ManagePostDownload
from local.artifacts.DownloadApplication import DownloadApplication
from util import FolderActions as Folder, FileActions as File
from web.api.teamcity import TeamCity


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
                    print "Incorrect TeamCity login credentials | url: {}".format(
                        get_dict_value(self.teamcity_setting, ["host"]))
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
        if database_connection:
            return database_connection
        else:
            return False

    def check_download_location_ready(self):
        download_location = get_dict_value(self.environment_setting, ["download_artifact_root_path"])
        copy_all_config_location = Folder.build_path(download_location,
                                                     get_dict_value(self.environment_setting,
                                                                    ["artifact_config_folder"]))
        if Folder.create_folder(download_location) and Folder.create_folder(copy_all_config_location):
            Folder.delete_folder_contents(folder_path=copy_all_config_location)
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
        download_handler = get_dict_value(app_details, ["SQL", "Download"])  # type: DownloadApplication
        if download_handler and download_handler.get_download_status():
            sql_script_name = get_dict_value(self.environment_setting, ["db_property", "db_script"])
            file_extension = sql_script_name.rsplit(".", 1)[1]
            if file_extension.lower() == 'sql':
                sql_path = Folder.build_path(download_handler.download_path, sql_script_name)
                if File.isfile(sql_path):
                    return sql_path
        return None

    def start_setup(self):
        logger = DeploymentLog(get_dict_value(self.environment_setting, ["download_artifact_root_path"]))

        total_database_time = None

        artifact_download = ManageApplicationDownload(app_setting=self.application_setting,
                                                      env_setting=self.environment_setting)

        # DownloadApplication all artifacts
        start_time = logger.time_it()
        artifact_download.download_application()
        # total download time
        total_download_time = logger.total_time(start=start_time, end=logger.time_it())

        application_details = artifact_download.get_application_details()  # type: dict

        # Post download task, eg. update config file
        post_download = ManagePostDownload(environment_setting=self.environment_setting,
                                           application_details=application_details)
        post_download.start_post_download_task()

        # Replace old with new artifacts
        artifact_replace = ManageApplicationReplace(application_details=application_details,
                                                    env_setting=self.environment_setting)
        start_time = logger.time_it()
        artifact_replace.replace_application()
        # total artifact replace time
        total_replace_time = logger.total_time(start=start_time, end=logger.time_it())

        application_details = artifact_replace.get_application_details()  # type: dict

        sql_path = self.get_sql_script(app_details=application_details)

        if sql_path:
            start_time = logger.time_it()
            Database.recreate_database_from_script(database_connection=self.get_database_connection(),
                                                   sql_path=sql_path,
                                                   env_setting=self.environment_setting)
            total_database_time = logger.total_time(start=start_time, end=logger.time_it())
            print "{}\n{}\nDatabase recreated\n{}\n{}".format(artifact_download.spacer_char_hyphen,
                                                              artifact_download.spacer_char_hyphen,
                                                              artifact_download.spacer_char_hyphen,
                                                              artifact_download.spacer_char_hyphen)

        logger.write_deployment_status(app_details=application_details)
        download_location = get_dict_value(self.environment_setting, ["download_artifact_root_path"])
        logger.write_database_info(sql_path=sql_path)
        logger.write_artifact_info(download_path=download_location)
        logger.write_time(time_download=total_download_time, time_replace=total_replace_time,
                          time_db=total_database_time)
