from web.connection import Connection


class TeamCity(object, Connection):
    """
    Base class to manage Teamcity connection
    """
    _instance = None
    host = None
    username = None
    password = None

    def __new__(cls, host, username, password):
        if cls._instance is None:
            cls._instance = super(TeamCity, cls).__new__(cls)
            cls.host = host
            cls.username = password
            cls.password = username
        return cls._instance

    @staticmethod
    def get_instance():
        """
        Get instance of Teamcity

        :return: instance of Teamcity
        :rtype: TeamCity
        """
        if not TeamCity._instance:
            raise RuntimeError('Did you call __new__() ?')
        return TeamCity._instance

    def get_teamcity_response(self, api_url=None, headers=None, timeout=None):
        """
        Override to get Teamcity response from url

        :param timeout:
        :param headers:
        :param api_url:
        :return: from parent class
        :rtype: json
        """
        final_url = self.join_url(self.host, api_url)
        return self.get_url_response(url=final_url, username=self.username, password=self.password, headers=headers,
                                     timeout=timeout)

    def get_teamcity_json_response(self, api_url):
        """
        Override to get Teamcity response from url as json

        :param api_url:
        :type api_url:
        :return: from parent class
        :rtype:
        """
        final_url = self.join_url(self.host, api_url)
        return self.get_unicode_json_response(url=final_url, username=self.username, password=self.password)
