import time

from config.manage_json_config import get_dict_value
from local.artifacts.replace import ReplaceApplication
from util import file_actions as File
from util import folder_actions as Folder
from util.os_process import close_running_process


class ManageApplicationReplace:
    spacer_char_hyphen = '-' * 50
    spacer_char_asterisk = '*' * 65
    download_application_root_path = None
    config_folder_path = None
    exclude_file_extension = []
    application_details = {}
    application_name_keys = []
    process_to_terminate = []

    def __init__(self, app_setting, env_setting):
        self.env_setting = env_setting
        self.download_application_root_path = get_dict_value(env_setting, ["download_artifact_root_path"])
        self.config_folder_path = Folder.build_path(self.download_application_root_path,
                                                    get_dict_value(env_setting, ["artifact_config_folder"]))
        self.exclude_file_extension = get_dict_value(env_setting, ["exclude_file_extension"])

        self.process_to_terminate = get_dict_value(env_setting, ["windows_process_to_stop"])

        self.application_details = app_setting
        self.application_name_keys = app_setting.keys()

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

    def __get_and_update_replace_list2(self):
        # tester function and should be removed in future
        for item in self.application_name_keys:
            app_name, replace_object = self.__create_replace_object(app_name=item)
            if replace_object is not 'None':
                self.application_details[item]['Replace'] = replace_object

    def __create_replace_object(self, app_name):
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

    def __extract_configuration_file(self, app_name):
        # If config file name is supplied
        if Folder.folder_exists(self.config_folder_path):
            app_object = get_dict_value(self.application_details, [app_name, "Download"])
            config_file_name = get_dict_value(self.application_details, [app_name, "config_file_name"])
            if config_file_name:
                config_source_path = File.search_file_first_occurrence(filename=config_file_name,
                                                                       search_path=app_object.download_path)
                if config_source_path:
                    config_destination_path = Folder.build_path(self.config_folder_path, config_file_name)
                    File.copy_from_to_file(source=config_source_path, destination=config_destination_path)
                    self.__replace_text_config_file_if_required(app_name=app_name, source_path=config_destination_path)

    def __replace_text_config_file_if_required(self, app_name, source_path):
        # replace text only if required and size of both the list matches
        find_text = get_dict_value(self.application_details, [app_name, "find_text"])
        replace_text = get_dict_value(self.application_details, [app_name, "replace_text"])
        if find_text and replace_text and len(find_text) == len(replace_text):
            # better to search and replace via xpath, which has to be implemented
            File.find_replace_text_many(file_path=source_path, find_text_list=find_text,
                                        replace_text_list=replace_text)

    def replace_application(self):
        # make list of applications to be replaced
        self.__get_and_update_replace_list()
        # extract and collect all config files into a folder
        map(self.__extract_configuration_file, self.application_name_keys)
        map(close_running_process, self.process_to_terminate)
        print "{}\n{}".format(self.spacer_char_asterisk, self.spacer_char_asterisk)
        for application in self.application_name_keys:
            app_handler = get_dict_value(self.application_details, [application, "Replace"])  # type: ReplaceApplication
            if app_handler:
                app_handler.replace_artifact()

    def get_application_details(self):
        return self.application_details
