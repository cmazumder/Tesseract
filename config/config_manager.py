from config.manage_json_config import get_json_as_dictionary, get_value_from_json_file

from util.Singleton import Singleton

from util.file_actions import file_exists


class ConfigLoadError(Exception):
    """Raise if error in loading Configuration file"""


class ConfigManager(Singleton):
    config_load_status = True  # type: bool  # Status if all configs are successfully loaded
    list_configs_failed = []  # type: list  # List of configs that could not be loaded

    master_config_with_path = None  # type: str  # Path of json config, for each individual config files
    artifacts_to_download_setting = None  # type: dict # config/json_config/artifacts_to_download.json
    environment_setting = None  # type: dict  # Load config/json_config/environment_setting.json
    database_setting = None  # type: dict  # Load config/json_config/local_database_setting.json
    teamcity_setting = None  # type: dict  # Load config/json_config/teamcity_setting.json

    def __init__(self, path_to_master_config):
        Singleton.__init__(self)
        self.master_config_with_path = path_to_master_config
        self.load_all_configurations()

    def load_config(self, setting_name):
        file_path = get_value_from_json_file(self.master_config_with_path, [setting_name])
        if file_path and file_exists(file_path):
            return get_json_as_dictionary(file_path).pop("_about", None)
        else:
            raise ConfigLoadError("Cannot load --> {}".format(setting_name))

    def load_teamcity(self):
        try:
            self.teamcity_setting = self.load_config("teamcity_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    def load_database(self):
        try:
            self.database_setting = self.load_config("local_database_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    def load_artifacts_to_download(self):
        try:
            self.artifacts_to_download_setting = self.load_config("artifacts_to_download")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    def load_environment_setting(self):
        try:
            self.environment_setting = self.load_config("environment_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    def get_teamcity(self):
        return self.teamcity_setting

    def get_database(self):
        return self.database_setting

    def get_artifacts_to_download(self):
        return self.artifacts_to_download_setting

    def get_environment_setting(self):
        return self.environment_setting

    def get_load_status(self):
        return self.config_load_status

    def get_list_of_failed_configs(self):
        return self.list_configs_failed

    def load_all_configurations(self):
        """Load all json configuration files.

        Args:
        Returns:
        Raises:
        """
        failed_config_name = []
        if self.load_teamcity():
            print "Got Teamcity config"
        else:
            print "Problem with Teamcity config"
            self.config_load_status = False
            self.list_configs_failed.append("TeamCity")

        if self.load_artifacts_to_download():
            print "Got application config"
        else:
            print "Problem with application config"
            self.config_load_status = False
            self.list_configs_failed.append("Application")

        if self.load_database():
            print "Got database config"
        else:
            print "Problem with database config"
            self.config_load_status = False
            self.list_configs_failed.append("Database")
