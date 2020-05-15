from os import path, makedirs, listdir, walk
from shutil import rmtree, copytree, move

from util.file_actions import file_exists, delete_file, compute_file_size


def delete_path(dir_path):
    try:
        if path.isdir(dir_path):
            rmtree(dir_path)
    except Exception as E:
        print E.message


def move_from_to_location(source, destination):
    delete_path(destination)
    try:
        move(source, destination)
        delete_path(source)
    except Exception as E:
        print E.message


def copy_from_to_location(source, destination):
    delete_path(destination)
    try:
        copytree(source, destination)
        return True
    except Exception as E:
        print E.message
        return False


def build_path(*args):
    file_path = r''
    try:
        for arg in args:
            file_path = path.join(file_path, arg)
    except Exception as E:
        print E.message
        raise Exception("Error in making os path <build_path>")
    return file_path


def folder_exists(folder_path):
    if path.isdir(folder_path):
        return True
    else:
        return False


def create_folder(folder_path):
    if folder_exists(folder_path=folder_path):
        return True
    else:
        try:
            makedirs(folder_path)
            return True
        except OSError as err:
            if not path.isdir(folder_path):
                raise OSError("Could not create {}".format(folder_path))
            print "OSError: {}".format(err.message)
        except WindowsError as err:
            print "WindowsError: {}".format(err.message)
    return False


def delete_folder_contents(folder_path):
    if folder_exists(folder_path):
        for item in listdir(folder_path):
            path = build_path(folder_path, item)
            if folder_exists(path):
                delete_path(path)
            elif file_exists(path):
                delete_file(path)


def get_folder_properties_file_count(folder_path):
    """Calculate the square root of a number.

    Args:
        folder_path: the path of the Folder
    Returns:
        no_of_file: total number of file as int.
    Raises:
        None
    """
    no_of_file = 0
    for dir_path, dir_names, file_names in walk(folder_path):
        for dirs in dir_names:
           pass
        for filename in file_names:
            no_of_file += 1
            return no_of_file


def get_folder_properties(folder_path):
    """Return no of files, sub-folder and size of a director

    Args:
        folder_path: the path of the Folder
    Returns:
        no of files, no of sub-folder and size
    Raises:
        none
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
