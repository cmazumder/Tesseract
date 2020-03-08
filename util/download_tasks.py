from os import path
from urllib import unquote

from requests import get

from util import folder_actions as Folder


def download_artifact_file(file_url, root_path, file_path_to_save, file_name, file_size):
    """
    
    """
    file_path_to_save = unquote(file_path_to_save)  # Replace %xx escapes by their single-character equivalent
    file_path_to_save = make_path_with_subfolder(root_path=root_path, file_name=file_name,
                                                 extract_subfolder_from_api=file_path_to_save)
    # print "file_path_to_save : {}\n file_name: {} PATH {}".format(file_path_to_save, file_name, file_path_to_save)
    if not file_path_to_save:
        print "file_path_to_save : {}\n file_name: {}".format(file_path_to_save, file_name)
    from_url_to_path(url=file_url, file_path=file_path_to_save)
    path_as_key = check_file_size(file_path=file_path_to_save, file_size=file_size)
    return path_as_key


def make_path_with_subfolder(root_path, file_name, extract_subfolder_from_api):
    try:
        if extract_subfolder_from_api == extract_subfolder_from_api.rsplit('/', 1)[0]:
            # subdirectory is not present, hence build straightforward path
            return Folder.build_path(root_path, file_name)
        else:
            extract_subfolder_from_api = extract_subfolder_from_api.rsplit('/', 1)[0]
            file_download_path = Folder.build_path(root_path, *extract_subfolder_from_api.split("/"))
            if Folder.create_folder(file_download_path):
                return Folder.build_path(file_download_path, file_name)
    except WindowsError:
        print "<make_path_with_subfolder>: {}".format(WindowsError.message)


def from_url_to_path(url, file_path):
    try:
        # print "URL {} PATH {}".format(url, file_path_to_save)
        with open(file_path, "wb") as file_download:
            response = get(url)
            file_download.write(response.content)
        file_download.close()
    except Exception as E:
        print "Error <from_url_to_path> \n\tMessage: {}\n\t f_path: {}\n\t url: {}".format(E.message,
                                                                                           file_path,
                                                                                           url)


def check_file_size(file_path, file_size):
    try:
        file_size_computed = str(path.getsize(file_path))
        if file_size_computed == file_size:
            return file_path
        else:
            print "File size differ for {} \n Actual size: {} Url size {}".format(file_path,
                                                                                  file_size_computed, file_size)
    except Exception as E:
        print "Error <check_file_size> {} \n file_path {} f_size {} ".format(E.message, file_path,
                                                                             file_size)
    except WindowsError:
        print "Error <check_file_size> {}".format(WindowsError.message)
