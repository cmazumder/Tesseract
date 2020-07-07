from config.manage_json_config import get_dict_value
from local.artifacts.UpdateConfigFile import UpdateConfigFile


class ManagePostDownload:
    config_update_setting = {}

    def __init__(self, config_update_setting):
        self.config_update_setting = config_update_setting
        # self.config_name = self.config_update_setting.keys()

    def modify_xml_config(self):
        for config_name in self.config_update_setting:
            xml_object = self._create_xml_edit_object(config_name=config_name)  # type: UpdateConfigFile
            xml_object.update_xml_config()

    def _create_xml_edit_object(self, config_name):
        """
        Create object of UpdateConfigFile
        @param config_name:
        @return: UpdateConfigFile
        @rtype: Object of UpdateConfigFile
        """
        return UpdateConfigFile(file_name=get_dict_value(self.config_update_setting, [config_name, "config_name"]),
                                file_path=get_dict_value(self.config_update_setting, [config_name, "config_path"]),
                                xml_attributes=get_dict_value(self.config_update_setting, [config_name, "attributes"]))
