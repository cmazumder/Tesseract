from util.XmlParser import XmlParser

def tmp_test():
    # set_attribute(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config",
    #                   xpath=".//fileNameConstraints[@enabled='true']", attrib="enabled", new_value="false")

    # set_attribute(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config",
    #                   xpath=".//system.diagnostics/switches/add[@new_value='Warning']", attrib="new_value", new_value="Verbose")

    # set_attribute(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config",
    #                   xpath=".//system.diagnostics/switches/add", attrib="new_value", new_value="Verbose")

    f1 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config"
    f2 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config"

    # parser = CommentedTreeBuilder()
    # tree = ET.parse(f1, parser)
    # tree.write(f2)

    xml_parser = XmlParser(file_path=f2)
    # tree = xml_parser.read_xml_file()
    # tree.write(file_or_filename=f2, encoding='UTF-8', xml_declaration=True)
    # xml_parser.set_attribute(xpath=".//fileNameConstraints[@enabled='true']", attrib="enabled", new_value="false")

    # xml_parser.set_attribute(xpath=".//system.diagnostics/switches/add", attrib="new_value",
    #                                   new_value="Verbose")

    xml_parser.set_attribute(xpath=".//appSettings/add[@key='PowerBackup']", attrib="value", new_value="")

    d1 = {"key": "QuixantDoorPin", "value": "Pin7"}
    xpath1 = ".//appSettings"
    element = 'add'
    xml_parser.add_element(xpath=xpath1, element=element, attrib_dict=d1)

tmp_test()