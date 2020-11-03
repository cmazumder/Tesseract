"""
Handle json
"""

import json
from os.path import normcase, dirname, abspath

import util.FileActions as File
import util.FolderActions as Folder


def get_dict_value(dictionary, keys, ascii=False, default=None):
    """
    Get value from nested dictionary using deep fetch

    Examples:
        * dictionary = {'meta': {'status': 'OK', 'status_code': 200}}
        * get_dict_value(dictionary, ["meta", "status_code"])          # => 200
        * get_dict_value(dictionary, ["garbage", "status_code"])       # => None
        * get_dict_value(dictionary, ["meta", "garbage"], default='-') # => '-'

    :param dictionary: dictionary to get value from
    :type dictionary: dict
    :param keys: list of keys for nested dictionary values
    :type keys: list
    :param ascii: specify if value has to returned as ascii
    :type ascii: bool
    :param default: return value if key not found. By default return None
    :type default: str
    :return: value from the dictionary
    :rtype: str
    """
    assert type(keys) is list
    if dictionary is None:
        return default
    if not keys:
        if ascii:
            return dictionary.encode('ascii', 'ignore')  # value converted from unicode
        else:
            return dictionary
    return get_dict_value(dictionary.get(keys[0]), keys[1:], default)


def get_path_from_json_file(json_file_path, val):
    """
    Get absolute path from master configuration files with path to all json configs

    :param json_file_path: path to master json file
    :type json_file_path: str
    :param val: the specific json file name
    :type val: str
    :return: relative path of the json file as per name in val
    :rtype: str
    """
    abs_file_path = get_abs_path(file_path=json_file_path)
    if abs_file_path:
        try:
            with open(abs_file_path, 'r') as config_file:
                dictionary = json.load(config_file)
                if dictionary:
                    return get_dict_value(dictionary, val)
        except IOError as err:
            print "I/O error({0}): {1}".format(err.errno, err.strerror)
    else:
        return False


def get_abspath_from_config(dictionary, val):
    """
    Get absolute path of file from the dictionary

    :param dictionary: contains filenames and relative paths
    :type dictionary: dict
    :param val: name of file
    :type val: str
    :return: absolute path of file
    :rtype: str
    """
    file_path = get_dict_value(dictionary, val)
    abs_file_path = get_abs_path(file_path=file_path)
    if abs_file_path:
        return file_path
    else:
        return False


def get_json_as_dictionary(json_file_path):
    """
    Parse json file and return as dictionary

    :param json_file_path: path to json file
    :type json_file_path: str
    :return: json as dictionary
    :rtype: dict
    """
    abs_file_path = get_abs_path(file_path=json_file_path)
    if abs_file_path:
        with open(abs_file_path, 'r') as config_file:
            return json.load(config_file)


def update_value_in_json_fie(json_file_path, dictionary):
    """
    Update value in json file from dictionary

    :param json_file_path: path to json file
    :type json_file_path: str
    :param dictionary: the values to update in json file
    :type dictionary: dict
    """
    abs_file_path = get_abs_path(file_path=json_file_path)
    if type(dictionary) is dict and dictionary:
        try:
            with open(abs_file_path, 'w') as config_file:
                json.dump(dictionary, config_file)
        except IOError as err:
            print "I/O error({0}): {1}".format(err.errno, err.strerror)


def get_abs_path(file_path):
    """
    Get absolute path to json file

    :param file_path: path of the file
    :type file_path: str
    :return: absolute os path of the file
    :rtype: str
    """
    file_path = abspath(file_path)
    if File.file_exists(file_path):
        return file_path
    else:
        return False


def force_abs_path(file_path):
    """

    :param file_path: relative path of file
    :type file_path: str
    :return: absolute path of file
    :rtype: str
    """
    script_dir = normcase(dirname(__file__))  # <-- absolute dir the script is in
    return Folder.build_path(script_dir, file_path)


def construct_abs_path(file_path):
    """
    Make absolute path for the relative path

    :param file_path: relative path of file
    :type file_path: str
    :return: absolute path of file
    :rtype: str
    """
    file_path = abspath(file_path)
    if File.file_exists(file_path):
        return file_path
    else:
        return False
