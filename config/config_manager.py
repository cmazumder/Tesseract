from config import setup_choice
from framework_config import teamcity_setting, vertex_buildTypeID, teamcity_download_setting
from local.database import Database
from util.connection import Connection


class ConfigManager:
    def __init__(self):
        pass

    def update_download_setting(self):
        """

        :return:
        :rtype:
        """
        try:
            # download vertex trunk builds
            if setup_choice["vertex"]["download"].lower() == 'yes':

                teamcity_download_setting.update(vertex_buildTypeID)
                teamcity_download_setting.update({"sql": {  # BuildTypeID for Vertex DataService
                    "buildTypeID": None,
                    "anchor": "SQL"
                }})
                return True
            # if user marked both Vertex and Nabler download as yes
            elif setup_choice["vertex"]["download"].lower() == 'yes' and \
                    setup_choice["nabler"]["download"].lower() == 'yes':
                print "Cannot setup Vertex and N-Abler artifacts together! Check config file"
                return False
        except (KeyError, NameError) as err:
            print "Error <ConfigManager> <update_download_setting>: {0}\nLists: {1}".format(err.message, err.args)
            return False

    def get_teamcity_api(self):
        try:
            if setup_choice["buildTypeID"].lower() == 'yes':
                teamcity_setting["api_buildId"] = r"app/rest/builds/buildType:{0},status:success"
                return True
            elif setup_choice["tag"]["download"].lower() == 'yes':
                teamcity_setting["api_buildId"] = r"app/rest/builds/buildType:{0},tags:({1})"
                return True
            elif setup_choice["buildTypeID"].lower() == 'yes' and \
                    setup_choice["tag"]["download"].lower() == 'yes':
                print "Cannot download using BuildTypeID and Tags together! Check config file"
                return False
        except (KeyError, NameError) as err:
            print "Error <ConfigManager> <update_download_setting>: {0}\nLists: {1}".format(err.message, err.args)
            return False

    def update_framework_config(self):
        if self.get_teamcity_api() and self.update_download_setting():
            return True
        else:
            return False

    def check_teamcity_available(self):
        teamcity = Connection()
        response = teamcity.get_url_response(url=teamcity_setting["host"],
                                             username=teamcity_setting["teamcity_username"],
                                             password=teamcity_setting["teamcity_username"])
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            print "Incorrect TeamCity login credentials"
            return False
        else:
            return False

    def check_database_connection(self):
        db = Database()
        if db.connect_to_db():
            return True
