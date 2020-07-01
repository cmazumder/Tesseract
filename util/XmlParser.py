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

    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.parser = ET.XMLParser(target=CommentedTreeBuilder())
        self.made_change_flag = False
        self.tree = self.get_xml_tree()
        self.root = self.tree.getroot()
        self.encoding = encoding

    def __del__(self):
        self.write_to_file()

    def read_xml_file(self):
        try:
            return ET.parse(source=self.file_path, parser=self.parser)
        except ET.ParseError as err:
            print "Error parsing code: {}\t Position: {}".format(err.code, err.position)

    def get_xml_tree(self):
        return self.read_xml_file()

    def set_attribute(self, xpath, attrib, new_value, encoding='utf-8'):
        s1 = self.root.find(xpath)

        if s1.get(str(attrib)):
            s1.set(str(attrib), str(new_value))
            self.made_change_flag = True

    def add_element(self, xpath, element, attrib_dict, encoding='utf-8'):
        s1 = self.tree.find(xpath)

        if s1.tag:
            # ele = ET.Element(str(element))
            sub_ele = ET.SubElement(s1, str(element), attrib_dict)
            sub_ele.tail = "\n"
            self.made_change_flag = True

    def indent_xml(self, elem, level=0):
        # required to indent xml properly if using add_element
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def write_to_file(self):
        if self.made_change_flag:
            file_root = dirname(self.file_path)
            temp_file = basename(self.file_path) + ".TMP"
            try:
                temp_file = join(file_root, temp_file)
            except Exception as err:
                print "Error joining filename: {}".format(err.message)

            self.indent_xml(elem=self.root, level=2)
            self.tree.write(file_or_filename=temp_file, encoding=self.encoding, xml_declaration=True)
            remove(self.file_path)
            rename(temp_file, self.file_path)
