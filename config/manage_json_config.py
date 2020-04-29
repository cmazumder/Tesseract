import json
from os.path import normcase, dirname, join

import util.file_actions as File


def get_dict_value_deep_fetch(dictionary, keys, ascii=False, default=None):
    """
    Example:
        dictionary = {'meta': {'status': 'OK', 'status_code': 200}}
        get_dict_value_deep_fetch(dictionary, ['meta', 'status_code'])          # => 200
        get_dict_value_deep_fetch(dictionary, ['garbage', 'status_code'])       # => None
        get_dict_value_deep_fetch(dictionary, ['meta', 'garbage'], default='-') # => '-'
    """
    assert type(keys) is list
    if dictionary is None:
        return default
    if not keys:
        if ascii:
            return dictionary.encode('ascii', 'ignore')  # value converted from unicode
        else:
            return dictionary
    return get_dict_value_deep_fetch(dictionary.get(keys[0]), keys[1:], default)


def get_value_from_json_file(json_file_path, val):
    abs_file_path = None
    if File.file_exists(json_file_path):
        abs_file_path = json_file_path
    else:
        script_dir = normcase(dirname(__file__))  # <-- absolute dir the script is in
        abs_file_path = join(script_dir, json_file_path)
    dictionary = None
    try:
        with open(abs_file_path, 'r') as config_file:
            dictionary = json.load(config_file)
            if dictionary:
                return get_dict_value_deep_fetch(dictionary, val)
    except IOError as err:
        print "I/O error({0}): {1}".format(err.errno, err.strerror)


def get_json_as_dictionary(json_file_path):
    abs_file_path = None
    if File.file_exists(json_file_path):
        abs_file_path = json_file_path
    else:
        script_dir = normcase(dirname(__file__))  # <-- absolute dir the script is in
        abs_file_path = join(script_dir, json_file_path)
    dictionary = None
    try:
        with open(abs_file_path, 'r') as config_file:
            dictionary = json.load(config_file)
            if dictionary:
                return dictionary
    except IOError as err:
        print "I/O error({0}): {1}".format(err.errno, err.strerror)


def update_value_in_json_fie(json_file_path, dictionary):
    abs_file_path = None
    if File.file_exists(json_file_path):
        abs_file_path = json_file_path
    else:
        script_dir = normcase(dirname(__file__))  # <-- absolute dir the script is in
        abs_file_path = join(script_dir, json_file_path)
    if type(dictionary) is dict and dictionary:
        try:
            with open(abs_file_path, 'w') as config_file:
                json.dump(dictionary, config_file)
        except IOError as err:
            print "I/O error({0}): {1}".format(err.errno, err.strerror)
