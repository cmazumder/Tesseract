import util.FileActions as File
import util.FolderActions as Folder
from config.manage_json_config import get_dict_value
from local.artifacts.ExtractConfigFiles import ExtractConfigFile
from local.artifacts.UpdateConfigFile import UpdateConfigFile


class ManagePostDownload:
    config_update_setting = {}
    application_details = {}

    def __init__(self, environment_setting, application_details):
        self.config_update_setting = get_dict_value(environment_setting, ["modify_config"])
        self.application_details = application_details
        self.config_root_location = Folder.build_path(
            get_dict_value(environment_setting, ["download_artifact_root_path"]),
            get_dict_value(environment_setting, ["artifact_config_folder"]))

    def modify_xml_config(self):
        for config_name in self.config_update_setting:
            xml_object = self._create_xml_edit_object(config_name=config_name)  # type: UpdateConfigFile
            if xml_object is not None:
                xml_object.update_xml_config()
            else:
                print "Did not modify --> {}".format(config_name)

    def _create_xml_edit_object(self, config_name):
        """
        Create object of UpdateConfigFile
        @param config_name:
        @return: UpdateConfigFile
        @rtype: Object of UpdateConfigFile
        """
        file_name = get_dict_value(self.config_update_setting, [config_name, "config_name"])
        file_root_path = get_dict_value(self.config_update_setting, [config_name, "config_path"])
        file_path = Folder.build_path(file_root_path, file_name)
        if File.file_exists(file_path):
            return UpdateConfigFile(file_name=file_name,
                                    file_path=file_path,
                                    xml_attributes=get_dict_value(self.config_update_setting,
                                                                  [config_name, "attributes"]))
        else:
            print "XML file not found at location {}".format(file_path)
            return None

    def extract_config_file(self):
        if Folder.folder_exists(self.config_root_location):
            config_extract_handler = ExtractConfigFile(config_folder_path=self.config_root_location,
                                                       application_details=self.application_details)
            config_extract_handler.start_extraction()

    def start_post_download_task(self):
        self.extract_config_file()
        self.modify_xml_config()
