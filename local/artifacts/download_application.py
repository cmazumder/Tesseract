from threading import Thread

from util import folder_actions as Folder
from website.api.application import Application


class DownloadApplication(Thread, Application):
    def __init__(self, app_name, download_artifact_root_path, folder_name, anchor_text, exclude_file_extension):
        Thread.__init__(self)
        self.application_name = app_name
        if not folder_name:
            self.download_path = download_artifact_root_path
        else:
            self.download_path = Folder.build_path(download_artifact_root_path, self.application_name)
        self.status = None
        if Folder.create_folder(self.download_path):
            Application.__init__(self, artifact_download_path=self.download_path,
                                 ignore_file_extensions=exclude_file_extension, anchor_text=anchor_text)
        else:
            print "{} not created".format(folder_name)

    def run(self):
        print self.spacer_char_asterisk
        print self.application_name
        self.__initiate_download()
        self.__print_download_status()
        print self.spacer_char_asterisk

    def __check_download_status(self):
        """
        Extract the config file only if count of download list and artifact list matches
        and if config file is there, and file name is passed as an argument
        """
        if self._count_of_download_and_artifact_list_match():
            folder_property = Folder.get_folder_properties(self.download_path)
            # counting if the number of actual downloaded files matches the count from the list
            if folder_property[0] == len(self.downloaded_file_details):
                self.status = True
            else:
                self.status = False

    def get_download_status(self):
        if self.status:
            return self.status

    def __print_download_status(self):
        self.__check_download_status()
        print self.spacer_char_hyphen
        if self.status:
            status_text = "OK"
        else:
            status_text = "BAD"
        print "{} \nDownloaded file status: {}".format(self.application_name, status_text)
        print self.spacer_char_hyphen

    def __initiate_download(self):
        self._start_download()
        self._show_downloaded_info()
