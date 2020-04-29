from website.connection import Connection


class TeamCity(Connection):
    host = None
    username = None
    password = None

    def __init__(self, host, username, password):
        Connection.__init__(self)
        self.host = host
        self.username = password
        self.password = username

    def get_teamcity_response(self, api_url, headers=None, timeout=None):
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
        self.get_url_response(url=final_url, username=self.username, password=self.password, headers=headers,
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
        self.get_json_response(url=final_url, username=self.username, password=self.password)
