from config.framework_config import teamcity_setting
from util.connection import Connection


class TeamCity(Connection):
    username = None
    password = None

    def __init__(self):
        try:
            self.username = teamcity_setting["teamcity_username"]
            self.password = teamcity_setting["teamcity_password"]
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)


