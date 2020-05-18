from config.manage_json_config import get_json_as_dictionary, get_value_from_json_file


class ConfigLoadError(Exception):
    """Raise if error in loading Configuration file"""


class ConfigManager(object):
    _instance = None
    config_load_status = None  # type: bool  # Status if all configs are successfully loaded
    list_configs_failed = []  # type: list  # List of configs that could not be loaded

    master_config_with_path = None  # type: str  # Path of json config, for each individual config files
    artifacts_to_download_setting = None  # type: dict # config/json_config/artifacts_to_download.json
    environment_setting = None  # type: dict  # Load config/json_config/environment_setting.json
    database_setting = None  # type: dict  # Load config/json_config/database_setting.json
    teamcity_setting = None  # type: dict  # Load config/json_config/teamcity_setting.json    

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not ConfigManager._instance:
            raise RuntimeError('Did you call __new__() ?')
        return ConfigManager._instance

    def __new__(cls, path_to_master_config):
        if cls._instance is None:
            print('Configuration Manager created')
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # Put any initialization here.
            cls.master_config_with_path = path_to_master_config
            cls.load_all_configurations()
        return cls._instance

    @classmethod
    def load_config(cls, setting_name):
        relative_path = get_value_from_json_file(cls.master_config_with_path, [setting_name])
        try:
            dictionary = get_json_as_dictionary(relative_path)
            if dictionary:
                del dictionary["_about"]
                return dictionary
            else:
                raise ConfigLoadError("Cannot load --> {}\nPath -->{}".format(setting_name, relative_path))
        except KeyError as err:
            print "Key error: {}".format(err.message)


    @classmethod
    def load_teamcity(cls):
        try:
            cls.teamcity_setting = cls.load_config("teamcity_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_database(cls):
        try:
            cls.database_setting = cls.load_config("database_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_artifacts_to_download(cls):
        try:
            cls.artifacts_to_download_setting = cls.load_config("artifacts_to_download")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_environment_setting(cls):
        try:
            cls.environment_setting = cls.load_config("environment_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def get_teamcity(cls):
        return cls.teamcity_setting

    @classmethod
    def get_database(cls):
        return cls.database_setting

    @classmethod
    def get_artifacts_to_download(cls):
        return cls.artifacts_to_download_setting

    @classmethod
    def get_environment_setting(cls):
        return cls.environment_setting

    @classmethod
    def get_load_status(cls):
        return cls.config_load_status

    @classmethod
    def get_list_of_failed_configs(cls):
        return cls.list_configs_failed

    @classmethod
    def load_all_configurations(cls):
        """Load all json configuration files.

        Args:
        Returns:
        Raises:
        """
        cls.config_load_status = True
        # Load TeamCity
        if cls.load_teamcity():
            print "Got Teamcity config"
        else:
            print "Problem with Teamcity config"
            cls.config_load_status = False
            cls.list_configs_failed.append("TeamCity")
        # Load application setting
        if cls.load_artifacts_to_download():
            print "Got application config"
        else:
            print "Problem with application config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Application")
        # Load Database setting
        if cls.load_database():
            print "Got database config"
        else:
            print "Problem with database config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Database")
        # Load environment setting
        if cls.load_environment_setting():
            print "Got environment config"
        else:
            print "Problem with environment config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Environment")
