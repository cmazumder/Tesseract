from urlparse import urljoin

from requests import get, ConnectionError


class Connection:

    def __init__(self):
        pass

    def get_json_response(self, url, username=None, password=None):
        header = {"Accept": "Application/JSON"}
        response_api = self.get_url_response(url, username=username, password=password, headers=header)
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

    def get_url_response(self, url, username=None, password=None, headers=None, timeout=None):
        """

        :param timeout:
        :param headers:
        :type headers:
        :param url:
        :type url:
        :param username:
        :type username:
        :param password:
        :type password:
        :return: response
        :rtype: json
        """
        try:
            response = get(url, auth=(username, password), headers=headers, timeout=timeout)
            return response
        except ConnectionError as err:
            print "Cannot connect\n Error #: {}\nMessage: {}\nRequest: {}".format(err.errno, err.message, err.request)
        print "No response from url: {}".format(url)

    def join_url(self, *args):
        """
        pythonic way to make urls
        WARNING Don't sent any argument starting with /
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
