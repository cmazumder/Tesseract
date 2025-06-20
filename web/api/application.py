"""
Manage artifacts/application details to be downloaded from TeamCity
"""

from urllib import unquote

from build import Build
from util import FolderActions as Folder, FileActions as File
from util.FileActions import basename
from util.ProgressBar import ProgressBar2


class Application(Build):
    """
    Derived class from Build to handle and save attributes of each artifacts to be downloaded from TeamCity.

    It's responsible for managing the download of but fetching the list of files from api and triggering the download
    and saving the files to the system
    """
    application_count = 0

    def __init__(self, app_name, artifact_download_path, ignore_file_extensions, anchor_text):
        Build.__init__(self)

        """ 
        artifact_file_details will save the information of the files to be downloaded in a dict
        artifact relative_path : [artifact api, file size, file name] 
        """
        self.artifact_file_details = {}

        """
        downloaded_file_details will save the information of the files downloaded in a dict
        absolute_path : FileName
        """
        self.application_name = app_name
        self.downloaded_file_details = {}  # type : dict

        # self.artifact_url_complete = None  # type : str
        self.url_resource_text = anchor_text.split("/")[-1]  # type : str
        self.save_to_path = artifact_download_path  # type : str
        self.anchor_text = anchor_text  # type : str
        self.exclude_file_extension = ignore_file_extensions  # type : list
        self.total_size = 0
        self.actual_application_count = 0

    def __del__(self):
        print "Files in artifact: {} \n" \
              "Files downloaded : {} \n".format(len(self.artifact_file_details), len(self.downloaded_file_details))

    def __create_filelist_from_api(self, artifact_list_from_api, filename_to_get=[]):
        """
        Private method
        create list of urls and file names that would be downloaded and also used to create subdirectories

        :param filename_to_get: list of filenames that has to be included in dict artifact_file_details
        :param artifact_list_from_api: api json response with list of files
        """
        try:
            for items in artifact_list_from_api["file"]:
                if "size" in items:  # it's a file
                    # exclude file with extension (if any extension is specified in config)
                    try:
                        if any(ext not in basename(items["content"]["href"]) for ext in
                               self.exclude_file_extension) \
                                or len(self.exclude_file_extension) == 0:
                            try:
                                if len(filename_to_get) == 0 or \
                                        any(file_name == basename(items["content"]["href"]) for file_name in
                                            filename_to_get):
                                    """
                                    Make values as list [
                                    u'/guestAuth/app/rest/builds/id:21210/artifacts/content/
                                    Aristocrat.Vertex.UI.Web/Aristocrat.Vertex.UI.Web.csproj',
                                    b'9389',
                                    ]
                                    """
                                    file_info = [items["content"]["href"], items["size"], items["name"]]
                                    self.total_size += items["size"]
                                    # Make the key as file path Eg Aristocrat.Vertex.UI.Web.csproj
                                    file_path = items["href"].split(self.url_resource_text, 1)[1][1:]
                                    self.artifact_file_details[file_path] = file_info
                            except TypeError as err:
                                print "TypeError at file filename check: {}\nArgs: {}".format(err.message, err.args)
                    except TypeError as err:
                        print "TypeError at file extension check: {}\nArgs: {}".format(err.message, err.args)
                else:  # it is directory, hence hit api again to find further files
                    url = items["children"]["href"]
                    updated_api_response = self.get_json_response_as_dict(url)
                    self.__create_filelist_from_api(artifact_list_from_api=updated_api_response,
                                                    filename_to_get=filename_to_get)
        except KeyError as err:
            print "KeyError as __create_filelist_from_api: {}\nArgs: {}".format(err.message, err.args)

    def __complete_download_prerequisite(self, artifact_repository_url):
        """
        Check if url is available then create the list of files to download from server (TeamCity)

        :param artifact_repository_url: url of artifact
        :type artifact_repository_url: str
        :return: status
        :rtype: bool
        """
        status = True
        if self.get_api_response_status(api_url=artifact_repository_url) == 200:
            response_as_dict = self.get_json_response_as_dict(artifact_repository_url)
            self.__create_filelist_from_api(artifact_list_from_api=response_as_dict)
            if not Folder.create_folder(self.save_to_path):
                status = False
        else:
            status = False
        return status

    def _initiate_download(self):
        """
        Start app file(s) download
        """
        # make the api for artifacts with the list of files
        artifact_url = self.teamcity_handler.join_url(self.application_api, self.anchor_text)

        if self.__complete_download_prerequisite(artifact_repository_url=artifact_url):
            Application.application_count += 1
            self.actual_application_count = Application.application_count
            self.__start_download()

    def __start_download(self):
        """
        Start download

        """
        # progress bar
        progress = ProgressBar2(desc=self.application_name, total=self.total_size,
                                position=self.actual_application_count, leave=True)
        for item in self.artifact_file_details:
            path_as_key = self.__download_file_from_api(file_api=self.artifact_file_details[item][0],
                                                        file_relative_path=item,
                                                        file_size=self.artifact_file_details[item][1])
            progress.bar.set_postfix_str(str(self.artifact_file_details[item][2]), refresh=False)
            progress.bar.update(self.artifact_file_details[item][1])

            if path_as_key:
                # key : value => file_path : file_name
                # split from right into 2 slices, the first element from right. Get just the filename
                self.downloaded_file_details[path_as_key] = self.artifact_file_details[item][0].rsplit("/", 1)[-1]
        progress.bar.close()

    def _count_of_download_and_artifact_list_match(self):
        """
        Check if count of list of files to download and files downloaded match

        :return: status
        :rtype: bool
        """
        if len(self.artifact_file_details) == len(self.downloaded_file_details):
            return True
        else:
            return False

    def show_downloaded_info(self):
        """
        Print version information

        """
        print "Version: {}\nBuild_ID: {}".format(self.version_number, self.build_id)
        print "Teamcity file count : {} \n" \
              "Downloaded file count : {}".format(len(self.artifact_file_details), len(self.downloaded_file_details))
        # print "---------Downloaded---------\n {}".format(json.dumps(self.downloaded_file_details, indent=4))

    def __download_file_from_api(self, file_api, file_relative_path, file_size):
        """
        Download and save file from the file_api list and save to system and return the absolute path of the file

        :param file_api: api of the file
        :type file_api: string
        :param file_relative_path: relative file path
        :type file_relative_path: string
        :param file_size: file size in bytes
        :type file_size: bytes
        :return: absolute file path from file_complete_path
        :rtype: str
        """
        file_relative_path = unquote(file_relative_path)  # Replace %xx escapes by their single-character equivalent

        # convert relative file path to win format and also create sub directories if required
        file_complete_path = self.__build_complete_windows_path(relative_path=file_relative_path)

        if not file_complete_path:
            print "Skipped file : {}".format(file_complete_path)
        self.__save_file_to_system(api_url=file_api, file_path=file_complete_path)
        if self.__file_size_match(file_path=file_complete_path, file_size=file_size):
            return file_complete_path

    def __build_complete_windows_path(self, relative_path):
        """
        Make absolute file path from relative file path for Application

        :param relative_path: relative file path
        :type relative_path: string
        :return: absolute file path
        :rtype: str
        """
        try:
            # split from right, the first element from left. Checking if relative path is the file itself
            if relative_path == relative_path.rsplit("/")[0]:
                # subdirectory is not present, hence build straightforward path
                return Folder.build_path(self.save_to_path, relative_path)
            else:
                # split and make only 2 slices, the first element from left. Get just the sub directories
                file_directory = relative_path.rsplit("/", 1)[0]

                # split all and send as list which will now only have subdirectories
                file_directory = Folder.build_path(self.save_to_path, *file_directory.split("/"))
                if Folder.create_folder(file_directory):
                    # split from right into 2 slices, the first element from right. Get just the filename
                    return Folder.build_path(file_directory, relative_path.rsplit("/", 1)[-1])
        except WindowsError:
            print "Issue while converting to windows path: {}".format(WindowsError.message)

    def __save_file_to_system(self, api_url, file_path):
        """
        Save a file from url to system, and is used by __download_file_from_api method

        :param api_url: file api
        :type api_url: str
        :param file_path: absolute file path to save
        :type file_path: str
        """
        try:
            # do not need to close file obj explicitly 
            with open(file_path, "wb") as local_file:
                response = self.get_api_response(api_url)  # type: 'requests.models.Response'
                local_file.write(response.content)
        except Exception as E:
            print "Error <__save_file_to_system> \n\tMessage: {}\n\t f_path: {}\n\t url: {}".format(E.message,
                                                                                                    file_path,
                                                                                                    api_url)

    def __file_size_match(self, file_path, file_size):
        """
        Compare file size for a file in file_path with expected size in file_size

        :param file_path: absolute file path
        :type file_path: str
        :param file_size: size of file
        :type file_size: bytes
        :return: True/False
        :rtype: bool
        """
        file_size_computed = File.compute_file_size(file_path=file_path)
        if file_size_computed == file_size:
            return True
        else:
            return False
