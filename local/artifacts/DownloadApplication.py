"""
Task for artifact downloads
"""

from threading import Thread

from ConfigManager.ConfigManager import ConfigManager
from ConfigManager.ManageJsonConfig import get_dict_value
from util import FolderActions as Folder
from web.api.application import Application


class DownloadApplication(Thread, Application):
    """
    Derived class from Application to manage artifacts downloads

    Tasks: Get build ID, setup folder and start download
    """
    ConfigurationManger = None

    def __init__(self, app_name, download_artifact_root_path, exclude_file_extension):
        Thread.__init__(self)
        self.ConfigurationManger = ConfigManager.get_instance()  # type: ConfigManager
        temp_application_setting = self.ConfigurationManger.get_artifacts_to_download()
        self.application_setting = get_dict_value(temp_application_setting, [app_name])
        if self.application_setting:
            self.folder_name = get_dict_value(self.application_setting, ["folder_name"])
            self.build_type_id = get_dict_value(self.application_setting, ["buildTypeID"])
            self.tags = get_dict_value(self.application_setting, ["tags"])
            if not self.folder_name:
                self.download_path = download_artifact_root_path
            else:
                self.download_path = Folder.build_path(download_artifact_root_path, self.folder_name)
                # remove previously downloaded contents in the same folder
                Folder.delete_folder(folder_path=self.download_path)
            Application.__init__(self, app_name=app_name, artifact_download_path=self.download_path,
                                 ignore_file_extensions=exclude_file_extension,
                                 anchor_text=get_dict_value(self.application_setting, ["anchor"]))
            self.status = None

    def run(self):
        """
        constructor for Thread
        """
        api = self.build_success_api()
        if self.has_successful_build(api_url=api):
            print "App: \'{0}\' | Version: {1}".format(self.application_name, self.get_version_number())
            self._initiate_download()
            self.__update_download_status()
        else:
            print "Application: {0} | No successful build".format(self.application_name)

    def build_success_api(self):
        """
        Get build ID of successful Teamcity artifact

        :return: buildID information/None
        :rtype: str
        """
        temp_teamcity_setting = self.ConfigurationManger.get_teamcity()
        if self.tags and self.build_type_id:
            api_success = get_dict_value(temp_teamcity_setting, ["api_buildId_with_tags"])
            api_success = api_success.format(self.build_type_id, ','.join(self.tags))

        elif self.build_type_id and not self.tags:
            api_success = get_dict_value(temp_teamcity_setting, ["api_buildId_without_tags"])
            api_success = api_success.format(self.build_type_id)
        else:
            api_success = None
        return api_success

    def _get_download_folder_ready(self):
        if self.folder_name:
            # remove previously downloaded contents in the same folder
            Folder.delete_folder(folder_path=self.download_path)

        # now recreate the folder
        if Folder.create_folder(self.download_path):
            print "Download folder created: {}".format(self.folder_name)
        else:
            print "Download folder creation error in \'{}\'".format(self.folder_name)

    def __update_download_status(self):
        """
        Extract the config file only if count of download list and artifact list matches
        and if config file is there, and file name is passed as an argument
        """
        if self._count_of_download_and_artifact_list_match():
            folder_property = Folder.get_folder_properties(self.download_path)
            # counting if the number of actual downloaded files matches the count from the list
            if folder_property[0] == len(self.downloaded_file_details):
                self.status = True
            else:
                self.status = False

    def get_download_status(self):
        """
        Get status of download of the entire artifact

        :return: True/False
        :rtype: bool
        """
        return self.status

    def get_download_folder(self):
        """
        Get downloaded path of the artifact

        :return: download_path
        :rtype: str
        """
        return self.download_path

    def print_download_status(self):
        """
        Print download status of artifact

        """
        if self.status:
            status_text = "GOOD"
        else:
            status_text = "BAD"
        print "Download status: {}".format(status_text)
