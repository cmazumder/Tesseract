from config.manage_json_config import get_dict_value
from local.artifacts.UpdateConfigFile import UpdateConfigFile
import util.FileActions as File
import util.FolderActions as Folder


class ManagePostDownload:
    config_update_setting = {}

    def __init__(self, config_update_setting):
        self.config_update_setting = config_update_setting
        # self.config_name = self.config_update_setting.keys()

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
                                xml_attributes=get_dict_value(self.config_update_setting, [config_name, "attributes"]))
        else:
            print "XML file not found at location {}".format(file_path)
            return None
