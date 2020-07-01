from os import remove, rename
from os.path import dirname, basename, join
from xml.etree import ElementTree as ET


class CommentedTreeBuilder(ET.TreeBuilder):
    # Need this to handle comments in an xml file
    # https://gist.github.com/jamiejackson/a37e8d3dacb33b2dcbc1
    def __init__(self, *args, **kwargs):
        super(CommentedTreeBuilder, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)


class XmlParser:

    def __init__(self, file_path):
        self.file_path = file_path
        self.parser = ET.XMLParser(target=CommentedTreeBuilder())

    def read_xml_file(self):
        return ET.parse(source=self.file_path, parser=self.parser)

    def replace_attribute_value(self, xpath, attrib, new_value, encoding='utf-8'):
        file_root = dirname(self.file_path)
        temp_file = basename(self.file_path) + ".TMP"
        temp_file = join(file_root, temp_file)
        replace_flag = False

        tree = self.read_xml_file()
        root = tree.getroot()
        s1 = root.find(xpath)

        if s1.attrib:
            s1.set(attrib, new_value)
            tree.write(file_or_filename=temp_file, encoding=encoding, xml_declaration=True)
            replace_flag = True

        if replace_flag:
            remove(self.file_path)
            rename(temp_file, self.file_path)


def tmp_test():
    # replace_attribute_value(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config",
    #                   xpath=".//fileNameConstraints[@enabled='true']", attrib="enabled", new_value="false")

    # replace_attribute_value(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config",
    #                   xpath=".//system.diagnostics/switches/add[@new_value='Warning']", attrib="new_value", new_value="Verbose")

    # replace_attribute_value(file_path=r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config",
    #                   xpath=".//system.diagnostics/switches/add", attrib="new_value", new_value="Verbose")

    f1 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Shell - Copy.config"
    f2 = r"C:\Users\mazumderc\Desktop\PythonSample\Configurations\Valyria - Copy.config"

    # parser = CommentedTreeBuilder()
    # tree = ET.parse(f1, parser)
    # tree.write(f2)

    xml_parser = XmlParser(file_path=f2)
    # tree = xml_parser.read_xml_file()
    # tree.write(file_or_filename=f2, encoding='UTF-8', xml_declaration=True)
    # xml_parser.replace_attribute_value(xpath=".//fileNameConstraints[@enabled='true']", attrib="enabled", new_value="false")
    xml_parser.replace_attribute_value(xpath=".//system.diagnostics/switches/add", attrib="new_value",
                                       new_value="Verbose")
