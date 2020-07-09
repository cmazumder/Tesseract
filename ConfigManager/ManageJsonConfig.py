import json
from os.path import normcase, dirname, abspath

import util.FileActions as File
import util.FolderActions as Folder


def get_dict_value(dictionary, keys, ascii=False, default=None):
    """ get value from nested dictionary using deep fetch
    Example:
        dictionary = {'meta': {'status': 'OK', 'status_code': 200}}
        get_dict_value(dictionary, ["meta", "status_code"])          # => 200
        get_dict_value(dictionary, ["garbage", "status_code"])       # => None
        get_dict_value(dictionary, ["meta", "garbage"], default='-') # => '-'
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
    val is list
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
    val is list
    """
    file_path = get_dict_value(dictionary, val)
    abs_file_path = get_abs_path(file_path=file_path)
    if abs_file_path:
        return file_path
    else:
        return False


def get_json_as_dictionary(json_file_path):
    abs_file_path = get_abs_path(file_path=json_file_path)
    if abs_file_path:
        with open(abs_file_path, 'r') as config_file:
            return json.load(config_file)


def update_value_in_json_fie(json_file_path, dictionary):
    abs_file_path = get_abs_path(file_path=json_file_path)
    if type(dictionary) is dict and dictionary:
        try:
            with open(abs_file_path, 'w') as config_file:
                json.dump(dictionary, config_file)
        except IOError as err:
            print "I/O error({0}): {1}".format(err.errno, err.strerror)


def get_abs_path(file_path):
    file_path = abspath(file_path)
    if File.file_exists(file_path):
        return file_path
    else:
        return False


def force_abs_path(file_path):
    script_dir = normcase(dirname(__file__))  # <-- absolute dir the script is in
    return Folder.build_path(script_dir, file_path)


def construct_abs_path(file_path):
    file_path = abspath(file_path)
    if File.file_exists(file_path):
        return file_path
    else:
        return False
