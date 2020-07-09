import util.FileActions as File
import util.FolderActions as Folder
from ConfigManager.ManageJsonConfig import get_dict_value, get_abspath_from_config
from local.DatabaseSetup import DatabaseSetup as Database
from local.ManageApplicationDownload import ManageApplicationDownload
from local.artifacts.DownloadApplication import DownloadApplication


class ManageAdditionalTask:
    application_details = {}
    environment_setting = {}
    database_connection = None

    def __init__(self, application_details, environment_setting, database_connection):
        self.application_details = application_details
        self.environment_setting = environment_setting
        self.database_connection = database_connection

    def _setup_new_database(self):
        sql_path = self.__make_downloaded_sql_script_path()
        if sql_path:
            # start_time = logger.time_it()
            Database.recreate_database_from_script(database_connection=self.database_connection,
                                                   sql_path=sql_path,
                                                   env_setting=self.environment_setting)
            # total_database_time = logger.total_time(start=start_time, end=logger.time_it())
            print "{}\n{}\nDatabase recreated\n{}\n{}".format(ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen)
            return sql_path
        return False

    def _create_database_backup(self):
        sql_path = self.__get_backup_sql_script_path()
        if sql_path:
            # start_time = logger.time_it()
            Database.execute_sql_script(sql_path=sql_path, database_connection=self.database_connection)
            return True
        return False

    def __make_downloaded_sql_script_path(self):
        # check if sql data is available
        download_handler = get_dict_value(self.application_details, ["SQL", "Download"])  # type: DownloadApplication
        if download_handler and download_handler.get_download_status():
            sql_script_name = get_dict_value(self.environment_setting, ["db_to_setup", "db_script"])
            file_extension = sql_script_name.rsplit(".", 1)[1]
            if file_extension.lower() == 'sql':
                sql_path = Folder.build_path(download_handler.download_path, sql_script_name)
                if File.isfile(sql_path):
                    return sql_path
        return None

    def __get_backup_sql_script_path(self):
        # check if sql data is available
        sql_script_path = get_abspath_from_config(self.environment_setting, ["sql_scripts_run"])
        if sql_script_path:
            file_extension = sql_script_path.rsplit(".", 1)[1]
            if file_extension.lower() == 'sql':
                return sql_script_path
        return False

    def database_task(self):
        database_replace_status = self._setup_new_database()
        if database_replace_status is True:
            database_backup_status = self._create_database_backup()
            print "Created backup: ".format(database_backup_status)
        return database_replace_status
