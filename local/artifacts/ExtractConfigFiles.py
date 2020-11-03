"""
Task for extraction of controller configuration files
"""

from ConfigManager.ManageJsonConfig import get_dict_value
from util import FileActions as File
from util import FolderActions as Folder


class ExtractConfigFile:
    """
       Class extract each controller configuration files to configuration folder for later use

       Tasks: Extract configuration files
       """
    def __init__(self, config_folder_path, application_details):
        self.config_folder_path = config_folder_path
        self.application_details = application_details
        self.application_name_keys = application_details.keys()

    def __extract_configuration_file(self, app_name):
        app_object = get_dict_value(self.application_details, [app_name, "Download"])
        config_file_name = get_dict_value(self.application_details, [app_name, "config_file_name"])
        if config_file_name:
            config_source_path = File.search_file_first_occurrence(filename=config_file_name,
                                                                   search_path=app_object.download_path)
            if config_source_path:
                config_destination_path = Folder.build_path(self.config_folder_path, config_file_name)
                File.copy_from_to_file(source=config_source_path, destination=config_destination_path)

    def start_extraction(self):
        """
        extract and collect all config files into a folder
        """
        map(self.__extract_configuration_file, self.application_name_keys)
