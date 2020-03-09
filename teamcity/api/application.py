from os import path
from threading import Thread

from build import Build
from config.framework_config import deployment_env_paths, teamcity_setting
from util import folder_actions as Folder, download_tasks as DownloadTask, file_actions as File


class Application(Build, Thread):
    spacer_char_hyphen = '-' * 50
    spacer_char_asterisk = '*' * 50

    def __init__(self):
        Thread.__init__(self)
        Build.__init__(self)

        """ 
        artifact_file_details <dictionary of list> 
        app_relative_path : [file_name, file_size, app_url_path] 
        """
        self.artifact_file_details = {}

        """
        downloaded_file_list <dictionary of downloaded files>
        Absolute path : FileName
        """
        self.downloaded_file_list = {}
        self.artifact_url_complete = None
        self.url_resource_text = None
        self.artifact_download_path = None
        self.anchor_text = None
        try:
            self.exclude_file_extension = deployment_env_paths["exclude_file_extension"]  # list of file extensions
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def __del__(self):
        print "File in teamcity: {} \n" \
              "Files downloaded: {} \n".format(len(self.artifact_file_details), len(self.downloaded_file_list))
        pass

    def set_file_download_path(self, save_artifact_dir):
        try:
            self.artifact_download_path = path.join(deployment_env_paths["path_download_root"],
                                                    save_artifact_dir)  # path to download
            if self.artifact_download_path != deployment_env_paths["path_download_root"]:
                # Don't delete root folder path_download_root
                Folder.delete_path(dir_path=self.artifact_download_path)
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def set_artifact_url(self, build_id, *url_resource):
        """
        Set base api url and
        :return: None
        """
        # self.artifact_url_complete = artifact_url  # url to artifacts
        try:
            api_artifact = teamcity_setting["api_artifacts"].format(build_id)
            self.artifact_url_complete = self.join_url(self.host, api_artifact, *url_resource)
            self.url_resource_text = str(url_resource[-1])  # url split marker to handle subdirectories
        except KeyError as err:
            print "Key error: {0}\nLists: {1}".format(err.message, err.args)
        except NameError as err:
            print "Name error: {0}\nLists: {1}".format(err.message, err.args)

    def create_filelist_from_api(self, api_response, filename_to_get=[]):
        """
        create list of urls and file names that would be downloaded and also used to create subdirectories
        :param filename_to_get: list of filenames that has to be included in dict artifact_file_details
        :param api_response: api json response with list of files
        """
        try:
            for items in api_response["file"]:
                if "size" in items:  # it's a file
                    # exclude file with extension (if any extension is specified in config)
                    try:
                        if any(ext not in File.path.basename(items["content"]["href"]) for ext in self.exclude_file_extension) \
                                or len(self.exclude_file_extension) == 0:
                            try:
                                if len(filename_to_get) == 0 or \
                                        any(file_name == File.path.basename(items["content"]["href"]) for file_name in filename_to_get):
                                    value = [items["name"], str(items["size"]), items["content"]["href"]]
                                    make_key = items["href"].split(self.url_resource_text, 1)[1][1:]
                                    self.artifact_file_details[make_key] = value
                            except TypeError as err:
                                print "TypeError at file filename check: {}\nArgs: {}".format(err.message, err.args)
                    except TypeError as err:
                        print "TypeError at file extension check: {}\nArgs: {}".format(err.message, err.args)
                else:  # it's a dir
                    url = self.join_url(self.host, items["children"]["href"])
                    updated_api_response = self.get_decoded_json_response(url)
                    self.create_filelist_from_api(api_response=updated_api_response, filename_to_get=filename_to_get)
        except KeyError as err:
            print "KeyError as create_filelist_from_api: {}\nArgs: {}".format(err.message, err.args)

    def download_files_from_list(self):
        """
        Check if url is available then download Vertex Service files
        :return: None
        """
        session_response = self.teamcity_session.get_url_response(url=self.artifact_url_complete,
                                                  username=self.teamcity_session.username,
                                                  password=self.teamcity_session.password)
        if session_response.status_code == 200:
            api_response = self.get_decoded_json_response(self.artifact_url_complete)
            self.create_filelist_from_api(api_response=api_response)
            self.start_download()

    def start_download(self):
        """
        start app file(s) download
        :return: None
        """
        if Folder.create_folder(self.artifact_download_path):
            for items in self.artifact_file_details:
                app_path_url = self.join_url(self.host, self.artifact_file_details[items][2])
                path_as_key = DownloadTask.download_artifact_file(file_url=app_path_url,
                                                                  root_path=self.artifact_download_path,
                                                                  file_path_to_save=items,
                                                                  file_name=self.artifact_file_details[items][0],
                                                                  file_size=self.artifact_file_details[items][1])
                if path_as_key:
                    # key : value => file_path : file_name
                    self.downloaded_file_list[path_as_key] = self.artifact_file_details[items][0]

    def compare_file_count(self):
        if len(self.artifact_file_details) == len(self.downloaded_file_list):
            return True
        else:
            return False

    def clear_artifact_list(self):
        self.artifact_file_details.clear()
        self.downloaded_file_list.clear()

    def show_downloaded_info(self):
        """
        temp func to print some info
        :return: None
        """
        print self.spacer_char_hyphen
        print "Version: {}\nBuild_ID: {}".format(self.version_number, self.build_id)
        print "Teamcity file count : {} \n" \
              "Downloaded file count : {} \n".format(len(self.artifact_file_details), len(self.downloaded_file_list))
        print self.spacer_char_hyphen
        # print "---------Downloaded---------\n {}".format(json.dumps(self.downloaded_file_list, indent=4))
