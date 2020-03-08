from requests import get, ConnectTimeout, ConnectionError
import sys


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

    def get_url_response(self, url, username=None, password=None, headers=None):
        """

        :param headers:
        :type headers:
        :param url:
        :type url:
        :param username:
        :type username:
        :param password:
        :type password:
        :return:
        :rtype:
        """
        try:
            response = get(url, auth=(username, password), headers=headers)
            return response
        except ConnectionError as err:
            print "Cannot connect (message): {}\n{}".format(err.message, err.request)
        except ConnectTimeout as err:
            print "Timeout {}:{}\n{}".format(err.errno, err.message, err.request)
        print "Terminating program"
        sys.exit(0)
