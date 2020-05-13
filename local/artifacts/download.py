from threading import Thread

from config.manage_json_config import get_dict_value
from infrastructure import configuration
from util import file_actions as File
from util import folder_actions as Folder
from website.api.application import Application

env_setting = configuration.get_environment_setting()


class Download(Thread, Application):
    save_artifact_root_path = get_dict_value(env_setting, ["save_artifact_root_path"])
    config_folder_path = Folder.build_path(save_artifact_root_path,
                                           get_dict_value(env_setting, ["artifact_config_folder"]))
    exclude_file_extension = get_dict_value(env_setting, ["exclude_file_extension"])
    Folder.create_folder(save_artifact_root_path)
    Folder.create_folder(config_folder_path)

    def __init__(self, folder_name, config_file_name, anchor_text, find_text, replace_text):
        Thread.__init__(self)
        self.application_name = folder_name
        self.config_file_name = config_file_name
        self.find_text = find_text
        self.replace_text = replace_text
        self.application_download_path = Folder.build_path(self.save_artifact_root_path, self.application_name)
        if Folder.create_folder(self.application_download_path):
            print "{} created".format(folder_name)
        else:
            print "{} not created".format(folder_name)
        Application.__init__(self, artifact_download_path=self.application_download_path,
                             ignore_file_extensions=self.exclude_file_extension, anchor_text=anchor_text)

    def download_application(self):

        self.service = Service()
        self.service.start()

        self.ui = UI()
        self.ui.start()

        self.shell = Shell()
        self.shell.start()

        self.dataservice = DataService()
        self.dataservice.start()

        self.reports = Reports()
        self.reports.start()

        self.service.join()
        self.ui.join()
        self.shell.join()
        self.dataservice.join()
        self.reports.join()

    def run(self):
        print self.spacer_char_asterisk
        print self.application_name
        self.download()
        print self.spacer_char_asterisk

    def extract_configuration_files(self):
        if Folder.folder_exists(self.config_folder_path):
            source_path = File.search_file_first_occurrence(filename=self.config_file_name,
                                                            search_path=self.application_download_path)
            if source_path:
                save_to_path = Folder.build_path(self.config_folder_path, self.config_file_name)
                if len(self.find_text) == len(self.replace_text):
                    # better to search and replace via xpath, which has to be implemented
                    File.find_replace_text_many(file_path=source_path, find_text=self.find_text,
                                                replace_text=self.replace_text)
                File.copy_from_to_file(source=source_path, destination=save_to_path)

    def download(self):
        self._start_download()
        self._show_downloaded_info()
        # Extract the config file only if count  download list and artifact list match and if config file name is present
        if self._count_of_download_and_artifact_list_match() and self.config_file_name:
            # check if downloaded file count and download list count matches
            folder_property = Folder.get_folder_properties(self.application_download_path)
            if folder_property[0] == len(self.downloaded_file_details):
                self.extract_configuration_files()
