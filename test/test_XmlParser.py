from util.XmlParser import XmlParser


def tmp_test_valyria():
    f2 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config"

    xml_parser = XmlParser(file_path=f2)
    # tree = xml_parser.read_xml_file()
    # tree.write(file_or_filename=f2, encoding='UTF-8', xml_declaration=True)

    # xml_parser.set_attribute(xpath=".//system.diagnostics/switches/add", element_attribute="element_value",
    #                                   element_value="Verbose")

    d_modify = {"value": ""}
    xpath_modify = ".//appSettings/add[@key='PowerBackup']"
    d_add = {"key": "QuixantDoorPin", "value": "Pin7"}
    xpath_add = ".//appSettings"
    tag = 'add'

    # old implementation
    # xml_parser.set_attribute(xpath=".//appSettings/add[@key='PowerBackup']", element_attribute="value",
    #                          element_value="")
    # xml_parser.add_element(xpath=xpath1, tag=tag, attribute_dict=d1)

    # xml_parser.modify_xml(xpath=xpath_add, tag=tag, attrib_dict=d_add)
    # xml_parser.modify_xml(xpath=xpath_modify, tag=tag, attrib_dict=d_modify)

    tag = None
    xml_parser.modify_xml(xpath=xpath_modify, tag=tag, attrib_dict=d_add)
    # xml_parser.modify_xml(xpath=xpath_modify, attrib_dict=d_add)


def tmp_test_shell():
    f1 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config"
    xpath = ".//fileNameConstraints[@enabled='true']"
    tag1 = "fileNameConstraints"
    tag = ""
    attribute = {"enabled": "false"}

    # xml_parser.set_attribute(xpath=".//fileNameConstraints[@enabled='true']", element_attribute="enabled", element_value="false")

    xml_parser = XmlParser(file_path=f1)
    xml_parser.modify_xml(xpath=xpath, tag=tag1, attrib_dict=attribute)


# tmp_test_valyria()
tmp_test_shell()
