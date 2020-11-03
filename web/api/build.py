"""
Basic information about artifacts/application details for download
"""

import json

from ConfigManager.ManageJsonConfig import get_dict_value
from web.api.teamcity import TeamCity


class Build:
    """
    Base class keep track of basic information of artifacts

    This class will check if api of artifact has a successful build or not. If yes, will save information related
    to build id and version number and api. These will be used to fetch future information and start download by
    derived call Application
    """
    def __init__(self):
        self.build_id = None
        self.version_number = None
        self.application_api = None
        self.host = None
        self.teamcity_handler = TeamCity.get_instance()

    def get_json_response_as_dict(self, api_url):
        """
        decoded json response from api / url

        :rtype: dict
        :return: json response
        """
        session_response = self.teamcity_handler.get_teamcity_json_response(api_url=api_url)
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
        session_response = self.teamcity_handler.get_teamcity_response(api_url=api_url)
        return session_response.status_code

    def get_api_response(self, api_url):
        """
        Response from api / url

        :rtype: string
        :return: http response
        """
        return self.teamcity_handler.get_teamcity_response(api_url=api_url)

    def has_successful_build(self, api_url):
        """
        List the last successfully completed build in TeamCity/server for the buildTypeId

        :param api_url: api url for teamcity
        :return: True if there is a successful build
        """
        response_teamcity = self.get_json_response_as_dict(api_url=api_url)
        if get_dict_value(dictionary=response_teamcity, keys=["status"], ascii=True) == 'SUCCESS':
            self.build_id = get_dict_value(dictionary=response_teamcity, keys=["id"], ascii=True)
            self.version_number = get_dict_value(dictionary=response_teamcity, keys=["number"], ascii=True)
            self.application_api = get_dict_value(dictionary=response_teamcity, keys=["artifacts", "href"])
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
        """
        Get the build id of artifact

        :return: build_id
        :rtype: str
        """
        return self.build_id

    def get_version_number(self):
        """
        Get the version number of artifact

        :return: version_number
        :rtype: str
        """
        return self.version_number

    def get_app_api(self):
        """
        Get the api url of artifact

        :return: application_api
        :rtype: str
        """
        return self.application_api
