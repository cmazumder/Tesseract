import json

from config.manage_json_config import get_dict_value_deep_fetch
from infrastructure import teamcity_handler


class Build:

    def __init__(self):
        self.build_id = None
        self.version_number = None
        self.application_api = None
        self.host = None

    def __del__(self):
        pass

    def get_json_response_as_dict(self, api_url):
        """
        decoded json response from api / url
        :rtype: dict
        :return: json response
        """
        session_response = teamcity_handler.get_teamcity_json_response(api_url=api_url)
        if session_response:
            return json.loads(session_response)
        else:
            return None

    def get_api_response_status(self, api_url):
        """
        Response from api / url
        :rtype: string
        :return: http response
        """
        session_response = teamcity_handler.get_teamcity_response(api_url=api_url)
        return session_response.status_code

    def get_api_response(self, api_url):
        """
        Response from api / url
        :rtype: string
        :return: http response
        """
        return teamcity_handler.get_teamcity_response(api_url=api_url)

    def has_successful_build(self, api_url):
        """
        List the last successfully completed build in teamcity_handler for the buildTypeId
        :param api_url: api url for teamcity
        :return: True if there is a successful build
        """
        response_teamcity = self.get_json_response_as_dict(api_url=api_url)
        if get_dict_value_deep_fetch(dictionary=response_teamcity, keys=["status"], ascii=True) == 'SUCCESS':
            self.build_id = get_dict_value_deep_fetch(dictionary=response_teamcity, keys=["id"], ascii=True)
            self.version_number = get_dict_value_deep_fetch(dictionary=response_teamcity, keys=["number"], ascii=True)
            self.application_api = get_dict_value_deep_fetch(dictionary=response_teamcity, keys=["artifacts", "href"])
            if self.build_id and self.version_number and self.application_api:
                return True
            else:
                print "Issue fetching info" \
                      "\nbuild_id: {}\nVersion: {}\napplication_api: {}".format(self.build_id,
                                                                                self.version_number,
                                                                                self.application_api)
                return False
        else:
            return False

    def get_build_id(self):
        return self.build_id

    def get_version_number(self):
        return self.version_number

    def get_app_api(self):
        return self.application_api

    def show_build_information(self):
        """
        Temp func to print info
        :return: None
        """
        print "BuildID: {} \n" \
              "Version: {} \n".format(self.build_id, self.version_number)
