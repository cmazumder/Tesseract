from threading import Thread

from config.config_manager import ConfigManager
from config.manage_json_config import get_dict_value
from util import folder_actions as Folder
from website.api.application import Application


class DownloadApplication(Thread, Application):
    ConfigurationManger = None

    def __init__(self, app_name, download_artifact_root_path, exclude_file_extension):
        Thread.__init__(self)
        self.ConfigurationManger = ConfigManager.get_instance()  # type: ConfigManager
        temp_application_setting = self.ConfigurationManger.get_artifacts_to_download()
        self.application_setting = get_dict_value(temp_application_setting, [app_name])
        if self.application_setting:
            self.application_name = app_name
            self.folder_name = get_dict_value(self.application_setting, ["folder_name"])
            self.build_type_id = get_dict_value(self.application_setting, ["buildTypeID"])
            self.tags = get_dict_value(self.application_setting, ["tags"])
            if not self.folder_name:
                self.download_path = download_artifact_root_path
            else:
                self.download_path = Folder.build_path(download_artifact_root_path, self.folder_name)
                # remove previously downloaded contents in the same folder
                Folder.delete_path(dir_path=self.download_path)
            Application.__init__(self, artifact_download_path=self.download_path,
                                 ignore_file_extensions=exclude_file_extension,
                                 anchor_text=get_dict_value(self.application_setting, ["anchor"]))
            self.status = None

    def run(self):
        print self.spacer_char_asterisk
        print "Application info: {}".format(self.application_name)

        api = self.build_success_api()
        if self.has_successful_build(api_url=api):
            print "Successful build version: {}".format(self.get_version_number())
            self._get_download_folder_ready()
            self.__initiate_download()
            self.__print_download_status()
        print self.spacer_char_asterisk

    def build_success_api(self):
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
            Folder.delete_path(dir_path=self.download_path)

        # now recreate the folder
        if Folder.create_folder(self.download_path):
            print "Download folder created: {}".format(self.folder_name)
        else:
            print "Download folder creation error in \'{}\'".format(self.folder_name)

    def __check_download_status(self):
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
        if self.status:
            return self.status

    def __print_download_status(self):
        self.__check_download_status()
        print self.spacer_char_hyphen
        if self.status:
            status_text = "OK"
        else:
            status_text = "BAD"
        print "{} \nDownloaded file status: {}".format(self.application_name, status_text)
        print self.spacer_char_hyphen

    def __initiate_download(self):
        self._start_download()
        self._show_downloaded_info()
