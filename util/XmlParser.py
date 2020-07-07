import re
from os import remove, rename
from os.path import dirname, basename, join
from xml.etree import ElementTree as ET


class DuplicateElement(Exception):
    def __init__(self, xpath, tag, attribute, message="Trying to add duplicate element?"):
        self.xpath = xpath
        self.element = self.make_emelemt_string(tag, attribute)
        self.message = message

    def __str__(self):
        error = self.message + "\nxpath -> {0}\nExists --> {1}".format(self.xpath, self.element)
        return error

    def make_emelemt_string(self, tag, attribute):
        attribute_list = " "
        for item in attribute:
            attribute_list += str(item) + "=\"" + str(attribute[item]) + "\""
            attribute_list += " "
        string = "<" + tag + " " + attribute_list + "/>"
        return string


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

    def __init__(self, file_path, indent_level=2, encoding='utf-8'):
        self.file_path = file_path
        self.parser = ET.XMLParser(target=CommentedTreeBuilder())
        self.xml_modified = False
        self.tree = self.get_xml_tree()
        self.root = self.tree.getroot()
        self.encoding = encoding
        self.indent_level = indent_level

    def __del__(self):
        if self.xml_modified:
            self.write_to_file()

    def read_xml_file(self):
        try:
            return ET.parse(source=self.file_path, parser=self.parser)
        except ET.ParseError as err:
            print "XML parse Error: {}\t Position: {}".format(err.code, err.position)

    def get_xml_tree(self):
        return self.read_xml_file()

    def find_element_by_xpath(self, xpath):
        return self.root.find(xpath)

    @staticmethod
    def get_tag_from_xpath(xpath):
        pattern_tag = r"/.*/(.*?)\["
        tag_curr = re.search(pattern_tag, xpath)
        if tag_curr is not None:
            return tag_curr.group(1)
        else:
            return None

    @staticmethod
    def get_key_from_xpath(xpath):
        pattern_key = r"@(.*?)="
        key = re.search(pattern_key, xpath)
        if key is not None:
            return key.group(1)
        else:
            return None

    @staticmethod
    def get_value_from_xpath(xpath):
        pattern_value = r"{}=\'(.*?)\'".format(XmlParser.get_key_from_xpath(xpath))
        value = re.search(pattern_value, xpath)
        if value is not None:
            return value.group(1)
        else:
            return None

    @staticmethod
    def check_duplicate_element(xpath, parent_node, tag, attrib_dict):
        sub_node_iter = parent_node.iterfind(str(tag))
        for element in sub_node_iter:
            if attrib_dict == element.attrib:
                raise DuplicateElement(xpath=xpath, tag=tag, attribute=element.attrib)

    def get_parent_node(self, xpath, tag, attrib_dict):
        parent_node = self.find_element_by_xpath(xpath)
        if parent_node is not None:
            XmlParser.check_duplicate_element(xpath=xpath, parent_node=parent_node, tag=tag, attrib_dict=attrib_dict)
        return parent_node

    def modify_xml(self, xpath, attrib_dict, tag=""):
        if tag == "":
            tag = XmlParser.get_tag_from_xpath(xpath=xpath)
        try:
            parent_node = self.get_parent_node(xpath=xpath, tag=tag, attrib_dict=attrib_dict)
            if parent_node is not None and parent_node.tag != tag:
                self.add_element(parent_node=parent_node, tag=tag, attribute_dict=attrib_dict)
            elif parent_node is not None:
                for key, value in attrib_dict.iteritems():
                    self.set_attribute(node=parent_node, element_attribute=key, element_value=value)

        except DuplicateElement as err:
            print err
            print "Add --> | Tag:{1} |Attributes {2}\n".format(xpath, tag, attrib_dict)

    def set_attribute(self, node, element_attribute, element_value):
        node.set(str(element_attribute), str(element_value))
        self.xml_modified = True

    def add_element(self, parent_node, tag, attribute_dict):
        sub_ele = ET.SubElement(parent_node, str(tag), attribute_dict)
        sub_ele.tail = "\n"
        self.xml_modified = True

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
        if self.xml_modified:
            file_root = dirname(self.file_path)
            temp_file = basename(self.file_path) + ".TMP"
            try:
                temp_file = join(file_root, temp_file)
            except Exception as err:
                print "Error joining filename: {}".format(err.message)

            self.indent_xml(elem=self.root, level=self.indent_level)
            self.tree.write(file_or_filename=temp_file, encoding=self.encoding, xml_declaration=True)
            remove(self.file_path)
            rename(temp_file, self.file_path)
