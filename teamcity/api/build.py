import json
from urlparse import urljoin

from framework_config import teamcity_setting
from teamcity import TeamCity as TeamCityUser


class Build:

    def __init__(self):
        try:
            self.host = teamcity_setting["host"]
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)
        build_id = None
        build_version_number = None
        api_url = None
        self.teamcity_session = TeamCityUser()
        self.set_api_url()

    def __del__(self):
        pass

    def join_url(self, *args):
        """
        pythonic way to make urls
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

    def get_decoded_json_response(self, url):
        """
        decoded json response from api / url
        :rtype: object
        :param url: api base path
        :return: json
        """
        teamcity_url = self.join_url(self.host, url)
        session_response = self.teamcity_session.get_json_response(url=teamcity_url,
                                                                   username=self.teamcity_session.username,
                                                                   password=self.teamcity_session.password)
        if session_response:
            return json.loads(session_response)
        else:
            return None

    def get_buildId_from_buildTypeId(self, buildTypeId):
        """
        List the last successfully completed build in teamcity for the buildTypeId
        :param buildTypeId: Team city project branch
        :return: List with api download_path_local and build number of the last successful build
        """
        build_information = self.get_decoded_json_response(self.api_url.format(buildTypeId))
        if build_information["status"] == u'SUCCESS':
            self.extract_info_from_json(build_info_json=build_information)
            return self.build_id
        else:
            return None

    def set_api_url(self):
        self.api_url = teamcity_setting["api_buildId"]

    def extract_info_from_json(self, build_info_json):
        """
        Save required info from json response
        :param build_info_json:
        :return: None
        """
        self.build_id = build_info_json["id"]  # value is int
        self.build_version_number = build_info_json["number"].encode('ascii', 'ignore')  # value converted from unicode

    def show_build_information(self):
        """
        Temp func to print info
        :return: None
        """
        print "BuildID: {} \n" \
              "Version: {} \n".format(self.build_id, self.build_version_number)
