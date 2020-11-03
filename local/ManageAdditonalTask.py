"""
Task such as setting up database and cleanup
"""

import util.FileActions as File
import util.FolderActions as Folder
from ConfigManager.ManageJsonConfig import get_dict_value, get_abspath_from_config
from local.DatabaseSetup import DatabaseSetup as Database
from local.ManageApplicationDownload import ManageApplicationDownload
from local.artifacts.DownloadApplication import DownloadApplication
from util.OSProcess import close_running_process


class ManageAdditionalTask:
    """
    This class will manage additional tasks of setup such as:
        - Get the right SQL script to use for creation of database
        - Create database backup, as this is required in RAM clear scenarios
        - Cleanup directories as specified in config file. E.g. Logs and database backups

    :param application_details: application details
    :type application_details: dict
    :param environment_setting: environment details
    :type environment_setting: dict
    :param database_connection: Database connection
    :type database_connection: DatabaseSetup
    """
    application_details = {}
    environment_setting = {}
    database_connection = None

    def __init__(self, application_details, environment_setting, database_connection):
        self.application_details = application_details
        self.environment_setting = environment_setting
        self.database_connection = database_connection
        self.process_to_terminate = get_dict_value(self.environment_setting, ["windows_process_to_stop"])

    def _setup_new_database(self):
        sql_path = self.__make_downloaded_sql_script_path()
        if sql_path:
            # start_time = logger.time_it()
            Database.recreate_database_from_script(database_connection=self.database_connection,
                                                   sql_path=sql_path,
                                                   env_setting=self.environment_setting)
            # total_database_time = logger.elapsed_time(start=start_time, end=logger.time_it())
            print "{}\n{}\nDatabase recreated\n{}\n{}".format(ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen,
                                                              ManageApplicationDownload.spacer_char_hyphen)
            return True
        return False

    def _create_database_backup(self):
        sql_path = self.__get_backup_sql_script_path()
        if sql_path:
            # start_time = logger.time_it()
            Database.execute_sql_script(sql_path=sql_path, database_connection=self.database_connection)
            return True
        return False

    def __make_downloaded_sql_script_path(self):
        """
        Make absolute path and check if it is the right sql script

        :return: path of the correct downloaded SQL script if present, else None
        :rtype: str/None
        """
        download_handler = get_dict_value(self.application_details, ["SQL", "Download"])  # type: DownloadApplication
        sql_script_name = get_dict_value(self.environment_setting, ["db_to_setup", "db_script"])
        if download_handler and download_handler.get_download_status() and sql_script_name is not None:
            file_extension = sql_script_name.rsplit(".", 1)[1]
            if file_extension.lower() == 'sql':
                sql_path = Folder.build_path(download_handler.download_path, sql_script_name)
                if File.isfile(sql_path):
                    return sql_path
        return None

    def __get_backup_sql_script_path(self):
        """
        Get sql script path if available

        :return: path of the correct downloaded SQL script if present, else False
        :rtype: str/bool
        """
        sql_script_path = get_abspath_from_config(self.environment_setting, ["sql_scripts_run"])
        if sql_script_path:
            file_extension = sql_script_path.rsplit(".", 1)[1]
            if file_extension.lower() == 'sql':
                return sql_script_path
        return False

    def database_task(self):
        """
        After creating new database, create backup database
        :return: status
        :rtype: bool
        """
        database_replace_status = self._setup_new_database()
        if database_replace_status is True:
            database_backup_status = self._create_database_backup()
            print "Created backup: {}".format(database_backup_status)
        return database_replace_status

    def delete_directory_contents(self):
        """
        Delete contents of folder/dir as per list in config file "cleanup_directories"

        """
        directory_to_clean = get_dict_value(self.environment_setting, ["cleanup_directories"])
        if directory_to_clean is not None:
            map(ManageAdditionalTask.__delete_content, directory_to_clean)

    @staticmethod
    def __delete_content(directory_list):
        if len(directory_list) > 1:
            Folder.delete_folder_contents(folder_path=directory_list[0], exclude_content=directory_list[1])
        else:
            Folder.delete_folder_contents(folder_path=directory_list[0])

    def close_running_process(self):
        """
        Close running windows processes in the list process_to_terminate

        """
        if self.process_to_terminate is not None and len(self.process_to_terminate) > 0:
            # check if any process is listed to be terminated
            map(close_running_process, self.process_to_terminate)
