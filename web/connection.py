"""
Manage network connection via url
"""

from urlparse import urljoin

from requests import get, ConnectionError


class Connection:
    """
    Base class to make connection request to url

    This class take the responsibility to manage connection request, getting URL and Json responses
    """
    @classmethod
    def get_unicode_json_response(cls, url, username=None, password=None):
        """
        Get the Json response from url

        :param url: the url to get response from
        :type url: str
        :param username: optional user name for authentication if required
        :type username: str
        :param password: optional password for authentication if required
        :type password: str
        :return: response_api.text
        :rtype: unicode
        """
        header = {"Accept": "Application/JSON"}
        response_api = cls.get_url_response(url, username=username, password=password, headers=header)
        if response_api.status_code == 200:
            return response_api.text
        elif response_api.status_code == 404:
            print "url:{}\nReason:{} ".format(url, response_api.text)
            raise Exception("Not found access")
        elif response_api.status_code == 400:
            print "url:{}\nReason:{} ".format(url, response_api.text)
            raise Exception("Unauthorised access")
        elif response_api.status_code != 200:
            print "url:{}\nReason:{} ".format(url, response_api.text)
            raise Exception("Something else")
        return None

    @classmethod
    def get_url_response(cls, url, username=None, password=None, headers=None, timeout=None):
        """
        Get Response from url

        :param url: the url to get response from
        :type url: str
        :param username: optional user name for authentication if required
        :type username: str
        :param password: optional password for authentication if required
        :type password: str
        :param headers: lines sent by the client in a HTTP protocol transaction
        :type headers: dict
        :param timeout: Requests to stop waiting for a response after a given number of seconds
        :type timeout: float
        :return: response
        :rtype: requests.Response
        """
        try:
            response = get(url, auth=(username, password), headers=headers, timeout=timeout)
            return response
        except ConnectionError as err:
            print "Cannot connect\n Error #: {}\nMessage: {}\nRequest: {}".format(err.errno, err.message, err.request)
        print "No response from url: {}".format(url)

    @classmethod
    def join_url(cls, *args):
        """
        Pythonic way to make urls
        WARNING Don't send any argument starting with /

        :param args: all arguments to be joined
        :return: final url
        """
        url = None
        for arg in args:
            url = urljoin(url, arg)
            if url[-1] != '/':
                url += '/'
        if url[-1] == '/':
            return url[:-1]
        return url
