
from config.manage_json_config import get_dict_value
from util.XmlParser import XmlParser


class UpdateConfigFile:
    def __init__(self, file_name, file_path, xml_attributes):
        self.file_name = file_name
        self.file_path = file_path
        self.xml_attributes = xml_attributes
        self.xml = XmlParser(file_path=self.file_path)

    def __del__(self):
        self.xml.__del__()

    def update_xml_config(self):
        for attribute in self.xml_attributes:
            xpath = get_dict_value(self.xml_attributes, [attribute, "xpath"])
            tag = get_dict_value(self.xml_attributes, [attribute, "tag"], default="")
            attribute_dict = get_dict_value(self.xml_attributes, [attribute, "attribute"])
            if xpath and tag and attribute:
                self.xml.modify_xml(xpath=xpath, tag=tag, attrib_dict=attribute_dict)
