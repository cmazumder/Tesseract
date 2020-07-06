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
        error = self.message + "\nxpath -> {0}\nExisting element --> {1}".format(self.xpath, self.element)
        return error

    def make_emelemt_string(self, tag, attribute):
        attribute_list = " "
        for item in attribute:
            attribute_list += str(item) + "=\"" + str(attribute[item]) + "\""
            attribute_list += " "
        string = "<" + tag + " " + attribute_list + "/>"
        return string


class ModifySelfAttributeIdentifierValue(Exception):
    def __init__(self, xpath, key, value, message="Trying to modify self identifier supplied in xpath?"):
        self.mod_key = self.make_string(key, value)
        self.xpath = xpath
        self.message = message

    def __str__(self):
        error = self.message + "\nxpath -> {0}\nAttribute -> {1}".format(self.xpath, self.mod_key)
        return error

    def make_string(self, key, value):
        return "@{0}=\'{1}\'".format(key,value)


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
            print "Error parsing code: {}\t Position: {}".format(err.code, err.position)

    def get_xml_tree(self):
        return self.read_xml_file()

    def find_element_by_xpath(self, xpath):
        return self.root.find(xpath)

    def check_self_identifier_attribute_modification(self, xpath, tag, attrib_dict):
        pattern_key = "@(.*?)="
        key = re.search(pattern_key, xpath)
        if key:
            key = key.group(1)
            pattern_value = "{}=\'(.*?)\'".format(key)
            value = re.search(pattern_value, xpath)
            if value:
                value = value.group(1)
                try:
                    if attrib_dict[key] != value:
                        raise ModifySelfAttributeIdentifierValue(xpath=xpath, key=key, value=attrib_dict[key])
                except KeyError:
                    pass

    def check_duplicate_element(self, xpath, parent_node, tag, attrib_dict):
        sub_node_iter = parent_node.iterfind(str(tag))
        for element in sub_node_iter:
            if attrib_dict == element.attrib:
                raise DuplicateElement(xpath=xpath, tag=tag, attribute=element.attrib)

    def get_parent_node(self, xpath, tag, attrib_dict):
        parent_node = self.find_element_by_xpath(xpath)
        self.check_self_identifier_attribute_modification(xpath=xpath, tag=tag, attrib_dict=attrib_dict)
        self.check_duplicate_element(xpath=xpath, parent_node=parent_node, tag=tag, attrib_dict=attrib_dict)
        return parent_node

    def modify_xml(self, xpath, tag, attrib_dict):
        try:
            parent_node = self.get_parent_node(xpath=xpath, tag=tag, attrib_dict=attrib_dict)
            if parent_node.tag != tag:
                self.check_duplicate_element(parent_node=parent_node, tag=tag, attrib_dict=attrib_dict)
                self.add_element(parent_node=parent_node, tag=tag, attribute_dict=attrib_dict)
            elif parent_node.tag == tag:
                for key, value in attrib_dict.iteritems():
                    self.set_attribute(node=parent_node, element_attribute=key, element_value=value)

        except DuplicateElement as err:
            print err
            print "Add element error. Path {0}\tTag:{1}\tAttributes {2}\n".format(xpath, tag, attrib_dict)
        except ModifySelfAttributeIdentifierValue as err:
            print err

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
