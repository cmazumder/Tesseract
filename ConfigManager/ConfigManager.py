"""
Manage json configuration file(s)
"""

from ManageJsonConfig import get_json_as_dictionary, get_path_from_json_file


class ConfigLoadError(Exception):
    """
    Custom exception class!

    Raised if there is any error in loading Configuration file
    """


class ConfigManager(object):
    """
    Singleton class to handle and load configuration from json to dictionary

    Will read a json configuration file, and load it into a dictionary. These values will be then used as per need
    throughout the framework
    """
    _instance = None
    config_load_status = None  # type: bool  # Status if all configs are successfully loaded
    list_configs_failed = []  # type: list  # List of configs that could not be loaded

    master_config_with_path = None  # type: str  # Path of json config, for each individual config files
    artifacts_to_download_setting = None  # type: dict # configuration/artifacts_to_download_VERTEX.json
    environment_setting = None  # type: dict  # Load configuration/environment_setting_VERTEX.json
    database_setting = None  # type: dict  # Load configuration/database_setting.json
    teamcity_setting = None  # type: dict  # Load configuration/teamcity_setting.json

    @staticmethod
    def get_instance():
        """
        Get instance of ConfigManger
        :return: _instance
        :rtype: ConfigManager
        """
        if not ConfigManager._instance:
            raise RuntimeError('Did you call __new__() ?')
        return ConfigManager._instance

    def __new__(cls, path_to_master_config):
        """
        create only one instance of ConfigManager
        :param path_to_master_config: path to master json config file
        :type path_to_master_config: str
        :return _instance: object
        :rtype: ConfigManager
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            # Put any initialization here.
            cls.master_config_with_path = path_to_master_config
            cls.load_all_configurations()
        return cls._instance

    @classmethod
    def load_config(cls, setting_name):
        """
        Load config from file to dictionary
        :param setting_name: path of the specific configuration
        :type setting_name: str
        :return: dictionary
        :rtype: dict
        """
        relative_path = get_path_from_json_file(cls.master_config_with_path, [setting_name])
        dictionary = get_json_as_dictionary(relative_path)
        if dictionary:
            del dictionary["_comment"]
            return dictionary
        else:
            raise ConfigLoadError("Cannot Load --> {}\nPath -->{}".format(setting_name, relative_path))

    @classmethod
    def load_teamcity(cls):
        """
        Load TeamCity config from file to teamcity_setting
        :return: True/False
        :rtype: bool
        """
        try:
            cls.teamcity_setting = cls.load_config("teamcity_setting")
            if cls.teamcity_setting:
                return True
            else:
                return False
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_database(cls):
        """
        Load database config from file to database_setting
        :return: True/False
        :rtype: bool
        """
        try:
            cls.database_setting = cls.load_config("database_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_artifacts_to_download(cls):
        """
        Load artifact(s) details config from file to artifacts_to_download_setting
        :return: True/False
        :rtype: bool
        """
        try:
            cls.artifacts_to_download_setting = cls.load_config("artifacts_to_download")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def load_environment_setting(cls):
        """
        Load local environment config from file to environment_setting
        :return: True/False
        :rtype: bool
        """
        try:
            cls.environment_setting = cls.load_config("environment_setting")
            return True
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)
            return False

    @classmethod
    def get_teamcity(cls):
        """
        Get teamcity configuration
        :return: teamcity_setting
        :rtype: dict
        """
        return cls.teamcity_setting

    @classmethod
    def get_database(cls):
        """
        Get database configuration
        :return: database_setting
        :rtype: dict
        """
        return cls.database_setting

    @classmethod
    def get_artifacts_to_download(cls):
        """
        Get artifact configuration
        :return: artifacts_to_download_setting
        :rtype: dict
        """
        return cls.artifacts_to_download_setting

    @classmethod
    def get_environment_setting(cls):
        """
        Get local environment configuration
        :return: environment_setting
        :rtype: dict
        """
        return cls.environment_setting

    @classmethod
    def get_load_status(cls):
        """
        Get the status of all the configuration of files being loaded successfully or not
        :return: config_load_status
        :rtype: bool
        """
        return cls.config_load_status

    @classmethod
    def get_list_of_failed_configs(cls):
        """
        Get the list of all the configuration of files that failed to load
        :return: list_configs_failed
        :rtype: list
        """
        return cls.list_configs_failed

    @classmethod
    def load_all_configurations(cls):
        """
        Load all the configuration files to dictionary
        """
        cls.config_load_status = True
        # Load TeamCity
        if not cls.load_teamcity():
            print "Problem with Teamcity config"
            cls.config_load_status = False
            cls.list_configs_failed.append("TeamCity")
        # Load application setting
        if not cls.load_artifacts_to_download():
            print "Problem with application config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Application")
        # Load Database setting
        if not cls.load_database():
            print "Problem with database config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Database")
        # Load environment setting
        if not cls.load_environment_setting():
            print "Problem with environment config"
            cls.config_load_status = False
            cls.list_configs_failed.append("Environment")
