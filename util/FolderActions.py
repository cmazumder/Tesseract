"""
Standalone operations on folder(s)
"""

from os import makedirs, listdir, walk
from os.path import isdir, join
from shutil import rmtree, copytree, move

from util.FileActions import file_exists, delete_file, compute_file_size


def delete_folder(folder_path):
    """
    Delete the folder. Careful this will delete non-empty folder too

    :param folder_path: path to the folder
    :type folder_path: str
    """
    try:
        if folder_exists(folder_path):
            rmtree(folder_path)
        else:
            print "Cannot delete. Non-existent or not a folder: {}".format(folder_path)
    except WindowsError as err:
        print "Cannot delete folder: {}\nErr: {}".format(folder_path, err.message)


def move_from_to_location(source, destination):
    """
    Move folder from source to destination
    Note: The destination folder will be first deleted

    :param source: path of folder source
    :type source: str
    :param destination: path to destination where the folder will be moved
    :type destination: str
    """
    delete_folder(destination)
    try:
        move(source, destination)
        delete_folder(source)
    except Exception as E:
        print E.message


def copy_from_to_location(source, destination):
    """
    Copy folder from source to destination
    Note: The destination folder will be first deleted

    :param source: path of folder source
    :type source: str
    :param destination: path to destination where the folder will be moved
    :type destination: str
    """
    delete_folder(destination)
    try:
        copytree(source, destination)
        return True
    except WindowsError as err:
        print "Issue with SOURCE: {} DESTINATION: {}".format(source, destination)
        print "Err: {}".format(err.args)
    return False


def build_path(*args):
    """
    Join path to handled os paths

    :param args: all the params will be joined
    :type args: str
    :return: absolute path
    :rtype: str
    """
    file_path = r''
    try:
        for arg in args:
            # for windows, replace forward slash with backslash if present
            arg = arg.replace("/", "\\")
            file_path = join(file_path, arg)
    except Exception as E:
        print E.message
        print "Paths: {}".format(args)
        raise Exception("Error in making os path <build_path>")
    return file_path


def folder_exists(folder_path):
    """
    Check if folder is present

    :param folder_path: path to the folder
    :type folder_path: str
    :return: status
    :rtype: bool
    """
    if isdir(folder_path):
        return True
    else:
        return False


def create_folder(folder_path):
    """
    Create a new folder, if not already present

    :param folder_path: path to the folder
    :type folder_path: str
    :return: status
    :rtype: bool
    """
    if folder_exists(folder_path=folder_path):
        return True
    else:
        try:
            makedirs(folder_path)
            return True
        except OSError as err:
            if not isdir(folder_path):
                raise OSError("Could not create {}".format(folder_path))
            print "OSError: {}".format(err.message)
        except WindowsError as err:
            print "WindowsError: {}".format(err.message)
    return False


def delete_folder_contents(folder_path, exclude_content=None):
    """
    Delete contents of folder, and not the folder

    :param folder_path: path to the folder
    :type folder_path: str
    :param exclude_content: List of any file that will not be deleted
    :type exclude_content: list
    """
    try:
        if folder_exists(folder_path):
            if exclude_content is not None:
                for item in listdir(folder_path):
                    if item not in exclude_content:
                        path = build_path(folder_path, item)
                        if folder_exists(path):
                            delete_folder(path)
                        elif file_exists(path):
                            delete_file(path)
            else:
                for item in listdir(folder_path):
                    path = build_path(folder_path, item)
                    if folder_exists(path):
                        delete_folder(path)
                    elif file_exists(path):
                        delete_file(path)
        else:
            print "Cannot delete non existent folder: {}".format(folder_path)
    except WindowsError as err:
        print "Cannot delete folder: {}\nErr: {}".format(folder_path, err.message)


def get_folder_properties_file_count(folder_path):
    """
    Get the total number of files in folder

    :param folder_path: path to the folder
    :type folder_path: str
    :return: count of files
    :rtype: int
    """
    no_of_file = 0
    for dir_path, dir_names, file_names in walk(folder_path):
        for dirs in dir_names:
            pass
        for filename in file_names:
            no_of_file += 1
            return no_of_file


def get_folder_properties(folder_path):
    """
    Return no of files, sub-folder and size of a director

    :param folder_path: path to the folder
    :type folder_path: str
    :return: count of files, folders and total size
    :rtype: int, int, bytes
    """
    no_of_file = 0
    no_of_folder = 0
    total_size = 0
    for dir_path, dir_names, file_names in walk(folder_path):
        for dirs in dir_names:
            no_of_folder += 1
        for filename in file_names:
            no_of_file += 1
            file_path = build_path(dir_path, filename)
            total_size += compute_file_size(file_path)
    return no_of_file, no_of_folder, total_size


def convert_bytes(num):
    """
    Convert bytes to MB.... GB... etc

    :param num: size
    :type num: int
    :return: size
    :rtype: bytes
    """
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
