"""
Standalone operations on file(s)
"""

import io
from os import remove, rename, walk
from os.path import isdir, basename, dirname, join, isfile, getsize, islink
from shutil import move, copy2


def append_text_to_file(file_path, *args):
    """
    Append text to a file

    :param file_path: path of the file
    :type file_path: str
    :param args: collections of all text
    :type args: str
    """
    if isdir(file_path):
        print "Cannot write to dir: {}".format(file_path)
    else:
        try:
            with open(file_path, "a+") as file_:
                for statement in args:
                    file_.write(str(statement))
                file_.write("\n")
            file_.close()
        except IOError as err:
            print "Message: {}\n Args: {}".format(err.message, err.args)
            raise IOError


def file_exists(file_path):
    """
    Check if file is present

    :param file_path: path of the file
    :type file_path: str
    :return: True/False
    :rtype: bool
    """
    try:
        if isfile(file_path):
            return True
    except IOError as err:
        print "I/O error: {0}. File path: {1}".format(err.strerror, err.filename)
    return False


def delete_file(file_path):
    """
    Delete a file

    :param file_path: path of the file
    :type file_path: str
    """
    if file_exists(file_path):
        try:
            remove(file_path)
        except WindowsError as E:
            print E.message
    else:
        print "{} not present, and cannot delete".format(file_path)


def move_from_to_file(source, destination):
    """
    Move a file from source to destination

    :param source: path to the file source
    :type source: str
    :param destination: path of destination
    :type destination: str
    """
    delete_file(destination)
    try:
        move(source, destination)
    except WindowsError as E:
        print E.message


def find_replace_text(file_path, find_text, replace_text, encoding='ascii'):
    """
    Find and replace a text in text file

    :param file_path: path of the file
    :type file_path: str
    :param find_text: original text
    :type find_text: str
    :param replace_text: replace text
    :type replace_text: str
    :param encoding: encoding of file
    :type encoding: str
    """
    if file_exists(file_path):
        file_root = dirname(file_path)

        original_file = io.open(file_path, "r", encoding=encoding)

        temp_file_name = basename(file_path) + ".TMP"
        temp_file_name = join(file_root, temp_file_name)
        temp_file = io.open(temp_file_name, "w", encoding=encoding)

        for line in original_file:
            if find_text in line:
                temp_file.write(line.replace(find_text, replace_text))
            else:
                temp_file.write(line)
        original_file.close()
        temp_file.close()
        delete_file(file_path)
        rename(temp_file_name, file_path)


def find_replace_text_many(file_path, find_text_list, replace_text_list, encoding='ascii'):
    """
    Find and replace a list of texts in text file
    Keep tab of pairing the two list!

    :param file_path: path of the file
    :type file_path: str
    :param find_text_list: list of original text
    :type find_text_list: list
    :param replace_text_list: list of replace text
    :type replace_text_list: list
    :param encoding: encoding of file
    :type encoding: str
    """
    if file_exists(file_path):
        file_root = dirname(file_path)

        original_file = io.open(file_path, "r", encoding=encoding)

        temp_file_name = basename(file_path) + ".TMP"
        temp_file_name = join(file_root, temp_file_name)
        temp_file = io.open(temp_file_name, "w", encoding=encoding)
        try:
            for line in original_file:
                for find_text, replace_text in zip(find_text_list, replace_text_list):
                    try:
                        if find_text in line:
                            line = line.replace(find_text, replace_text)
                    except Exception as err:
                        print "Replace text many\nErr: {}\nArgs{}".format(err.message, err.args)
                        print "Find:{}\nReplace:{}\nLine:{}".format(find_text, replace_text, line)
                temp_file.write(line)
        except UnicodeDecodeError as err:
            print "UnicodeDecodeError: {}\nArgs{}".format(err.message, err.args)
        original_file.close()
        temp_file.close()

        delete_file(file_path)
        rename(temp_file_name, file_path)


def copy_from_to_file(source, destination):
    """
    Move a file from source to destination

    :param source: path to the file source
    :type source: str
    :param destination: path of destination
    :type destination: str
    :return: status
    :rtype: bool
    """
    if file_exists(source) and isdir(dirname(destination)):
        if basename(source) == basename(destination) and file_exists(destination):
            delete_file(destination)
        try:
            copy2(source, destination)
            return True
        except OSError as err:
            print "File copy error:\nSource:{}\nDestination{}".format(err.message, source, destination)
            return False


def search_file_first_occurrence(search_path, filename):
    """
    Search for a file in folder

    :param search_path: path of the folder to search
    :type search_path: str
    :param filename: file to be searched
    :type filename: str
    :return: return absolute of file if found
    :rtype: str
    """
    result = r''
    # Waking top-down from the root
    for dir_path, dir_names, file_names in walk(search_path):
        if filename in file_names:
            result = join(dir_path, filename)
            return result


def search_file_all_occurrence(filename, search_path):
    """
    Search all the occurrence for a file in the folder

    :param search_path: path of the folder to search
    :type search_path: str
    :param filename: file to be searched
    :type filename: str
    :return: return absolute of file if found
    :rtype: list
    """
    result = []
    # Waking top-down from the root
    for dir_path, dir_names, file_names in walk(search_path):
        if filename in file_names:
            result.append(join(dir_path, filename))
    return result


def create_file(file_path, encoding='ascii'):
    """
    Create an empty file

    :param file_path: path of the file to be created
    :type file_path: str
    :param encoding: file encoding
    :type encoding: str
    """
    with io.open(file_path, "w", encoding=encoding) as file_write:
        file_write.close()


def compute_file_size(file_path):
    """
    Return size of the file

    :param file_path: path to file
    :type file_path: str
    :return: file size
    :rtype: bytes
    """
    if file_exists(file_path):
        # skip if it is symbolic link
        if not islink(file_path):
            return getsize(file_path)
    else:
        return None
