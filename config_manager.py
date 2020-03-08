from config import setup_choice
from framework_config import teamcity_setting, vertex_buildTypeID, teamcity_download_setting
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
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)
        return False

    def get_teamcity_api(self):
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

    def update_framework_config(self):

        if self.get_teamcity_api() and self.update_download_setting():
            return True
        else:
            return False

    def check_connection(self):
        teamcity = teamcity_setting["host"]
        timeout = 5
        try:
            _ = Connection.get_url_response(teamcity)
            return True
        finally:
            print "Cannot connect to Teamcity"
            return False
