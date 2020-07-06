from util.XmlParser import XmlParser


def tmp_test():
    f1 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config"
    f2 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config"

    # parser = CommentedTreeBuilder()
    # tree = ET.parse(f1, parser)
    # tree.write(f2)

    xml_parser = XmlParser(file_path=f2)
    # tree = xml_parser.read_xml_file()
    # tree.write(file_or_filename=f2, encoding='UTF-8', xml_declaration=True)
    # xml_parser.set_attribute(xpath=".//fileNameConstraints[@enabled='true']", element_attribute="enabled", element_value="false")

    # xml_parser.set_attribute(xpath=".//system.diagnostics/switches/add", element_attribute="element_value",
    #                                   element_value="Verbose")

    d_add = {"key": "QuixantDoorPin", "value": "Pin7"}
    d_modify = {"value": ""}
    xpath_modify = ".//appSettings/add[@key='PowerBackup']"
    xpath_add = ".//appSettings"
    tag = 'add'

    # old implementation
    # xml_parser.set_attribute(xpath=".//appSettings/add[@key='PowerBackup']", element_attribute="value",
    #                          element_value="")
    # xml_parser.add_element(xpath=xpath1, tag=tag, attribute_dict=d1)

    # xml_parser.modify_xml(xpath=xpath_add, tag=tag, attrib_dict=d_add)
    # xml_parser.modify_xml(xpath=xpath_modify, tag=tag, attrib_dict=d_modify)
    xml_parser.modify_xml(xpath=xpath_modify, tag=tag, attrib_dict=d_add)


tmp_test()
