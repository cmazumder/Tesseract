"""
Task to manage application replace
"""

from ConfigManager.ManageJsonConfig import get_dict_value
from local.artifacts.DownloadApplication import DownloadApplication
from local.artifacts.ReplaceApplication import ReplaceApplication
from util import FolderActions as Folder


class ManageApplicationReplace:
    """
    This class will handled replacement of artifacts.
    Delete old artifact and copy the new downloaded artifact(s)

    """
    spacer_char_hyphen = '-' * 50
    spacer_char_asterisk = '*' * 65
    download_application_root_path = None
    config_folder_path = None
    application_details = {}
    application_name_keys = []

    def __init__(self, application_details, env_setting):
        self.env_setting = env_setting
        self.download_application_root_path = get_dict_value(env_setting, ["download_artifact_root_path"])
        self.config_folder_path = Folder.build_path(self.download_application_root_path,
                                                    get_dict_value(env_setting, ["artifact_config_folder"]))
        self.application_details = application_details
        self.application_name_keys = application_details.keys()

    def __get_and_update_replace_list(self):
        list_of_application_object = dict
        try:
            list_of_application_object = dict(
                map(self.__create_replace_object, self.application_name_keys))
        except TypeError as err:
            print "Issue creating ReplaceApplication:{}\nArgs{}".format(err.message, err.args)

        for replace_object in list_of_application_object:
            if list_of_application_object[replace_object] is not 'None':
                self.application_details[replace_object]['Replace'] = list_of_application_object[replace_object]

    def __create_replace_object(self, app_name):
        """
        Create instance of ReplaceApplication

        :param app_name: Name of artifact
        :type app_name: str
        :return: Artifact name and ReplaceApplication instance
        :rtype: str, ReplaceApplication
        """
        app_download_handler = get_dict_value(self.application_details,
                                              [app_name, "Download"])  # type: DownloadApplication
        if app_download_handler.get_download_status() is True:
            curr_app_destinations = get_dict_value(self.application_details, [app_name, "copy_artifacts_to_path"])
            curr_config_name = get_dict_value(self.application_details, [app_name, "config_file_name"])
            if curr_app_destinations or curr_config_name:
                curr_app_source = app_download_handler.download_path
                curr_config_destinations = get_dict_value(self.application_details, [app_name, "copy_config_to_path"])
                curr_config_source = None
                if curr_config_name and curr_config_destinations:
                    curr_config_source = Folder.build_path(self.config_folder_path, curr_config_name)
                # create replacement object, since have replacement destination
                return app_name, ReplaceApplication(app_source=curr_app_source, app_destinations=curr_app_destinations,
                                                    config_source=curr_config_source,
                                                    config_destinations=curr_config_destinations)
            else:
                print "\'{}\' not meant to be replaced, skip replacement instance".format(app_name)
                return app_name, 'None'
        else:
            print "\'{}\' not downloaded properly, skip replacement instance".format(app_name)
            return app_name, 'None'

    def replace_application(self):
        """
        Make list of applications to be replaced

        """
        self.__get_and_update_replace_list()
        print "{}\n{}".format(self.spacer_char_asterisk, self.spacer_char_asterisk)
        for application in self.application_name_keys:
            app_handler = get_dict_value(self.application_details, [application, "Replace"])  # type: ReplaceApplication
            if app_handler:
                app_handler.replace_artifact()

    def get_application_details(self):
        """
        Get the application details

        :return: application_details
        :rtype: dict
        """
        return self.application_details
