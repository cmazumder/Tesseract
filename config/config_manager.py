from config.manage_json_config import get_json_as_dictionary, get_value_from_json_file
from local.database import Database
from util.Singleton import Singleton
from util.connection import Connection
from util.file_actions import file_exists


class ConfigLoadError(Exception):
    """Raise if error in loading Configuration file"""


class ConfigManager(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self.config_path = "config/json_config/config_path.json"
        self.application_structure_config = None
        self.deployment_evn_path_config = None
        self.database_config = None
        self.process_config = None
        self.teamcity_config = None

    def load_config(self, setting_name):
        file_path = get_value_from_json_file(self.config_path, [setting_name])
        if file_path and file_exists(file_path):
            return get_json_as_dictionary(file_path)
        else:
            raise ConfigLoadError("Cannot load --> {}".format(setting_name))

    def load_config_teamcity(self):
        try:
            self.teamcity_config = self.load_config("teamcity_config")
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)

    def load_config_database(self):
        try:
            self.database_config = self.load_config("local_database_setting")
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)

    def load_config_application_structure(self):
        try:
            self.application_structure_config = self.load_config("application_structure")
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)

    def load_config_deployment_evn(self):
        try:
            self.deployment_evn_path_config = self.load_config("deployment_evn_path")
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)

    def load_config_process(self):
        try:
            self.process_config = self.load_config("process_to_stop")
        except ConfigLoadError as err:
            print "Error: {0}".format(err.message)

    def get_config_teamcity(self):
        return self.teamcity_config

    def get_config_database(self):
        return self.database_config

    def get_config_application_structure(self):
        return self.application_structure_config

    def get_config_deployment_evn(self):
        return self.deployment_evn_path_config

    def get_config_process(self):
        return self.process_config

    def load_all_configurations(self):
        """
        Load all configuration files
        """
        self.load_config_teamcity()
        self.load_config_application_structure()
        self.load_config_database()
        self.load_config_deployment_evn()
        self.load_config_process()

    def check_teamcity_available(self):
        teamcity_config = get_value_from_json_file(self.config_path, ["teamcity_config"])
        teamcity = Connection()
        response = teamcity.get_url_response(url=get_value_from_json_file(teamcity_config, ["host"]),
                                             username=get_value_from_json_file(teamcity_config, ["teamcity_username"]),
                                             password=get_value_from_json_file(teamcity_config, ["teamcity_username"]))
        if response:
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print "Incorrect TeamCity login credentials"
                return False
        else:
            print "Cannot reach TeamCity"
            return False

    def check_database_connection(self):
        db = Database()
        if db.connect_to_db():
            return True
