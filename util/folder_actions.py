from os import path, makedirs, listdir
from shutil import rmtree, copytree, move

from util.file_actions import file_exists, delete_file


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
