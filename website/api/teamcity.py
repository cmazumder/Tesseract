from website.connection import Connection


class TeamCity(object, Connection):
    _instance = None
    host = None
    username = None
    password = None

    def __new__(cls, host, username, password):
        if cls._instance is None:
            print('Team City created')
            cls._instance = super(TeamCity, cls).__new__(cls)
            # Put any initialization here.
            cls.host = host
            cls.username = password
            cls.password = username
        return cls._instance

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not TeamCity._instance:
            raise RuntimeError('Did you call __new__() ?')
        return TeamCity._instance

    def get_teamcity_response(self, api_url=None, headers=None, timeout=None):
        """
            Re-implementation from superclass
            :param timeout:
            :param headers:
            :type string:
            :param api_url:
            :type string:
            :return: from parent class
            :rtype:
        """
        final_url = self.join_url(self.host, api_url)
        return self.get_url_response(url=final_url, username=self.username, password=self.password, headers=headers,
                              timeout=timeout)

    def get_teamcity_json_response(self, api_url):
        """
            Re-implementation from superclass
            :param api_url:
            :type api_url:
            :return: from parent class
            :rtype:
        """
        final_url = self.join_url(self.host, api_url)
        return self.get_json_response(url=final_url, username=self.username, password=self.password)
