"""
Update/modify controller config xml files
"""

from ConfigManager.ManageJsonConfig import get_dict_value
from util.XmlParser import XmlParser


class UpdateConfigFile:
    """
    This is a class manage all type of update and modification
    that would be required in an xml file(s)

    Task such as adding removing xml tag, attributes and etc.

    Be careful with extending the functionality, and if implementing any action on xml,
    be cautious and test thoroughly as it can lead to setup issues, and hard to trace root cause.

    :param file_name: xml file name
    :type file_name: str
    :param file_path: file path of xml
    :type file_path: str
    :param xml_attributes: store xml attributes and properties as key value
    :type xml_attributes: dict
    :param xml: xml handler
    :type xml: XmlParser

    """
    def __init__(self, file_name, file_path, xml_attributes):
        self.file_name = file_name
        self.file_path = file_path
        self.xml_attributes = xml_attributes
        self.xml = XmlParser(file_path=self.file_path)

    def __del__(self):
        self.xml.__del__()

    def update_xml_config(self):
        """
        Update xml attribute and property
        """
        for attribute in self.xml_attributes:
            xpath = get_dict_value(self.xml_attributes, [attribute, "xpath"])
            tag = get_dict_value(self.xml_attributes, [attribute, "tag"], default="")
            attribute_dict = get_dict_value(self.xml_attributes, [attribute, "attribute"])
            if xpath and tag and attribute:
                self.xml.modify_xml(xpath=xpath, tag=tag, attrib_dict=attribute_dict)
