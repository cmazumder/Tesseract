from config.manage_json_config import get_dict_value
from local.artifacts.DownloadApplication import DownloadApplication
from util import FolderActions as Folder


class ManageApplicationDownload:
    spacer_char_hyphen = '-' * 50
    spacer_char_asterisk = '*' * 65
    download_application_root_path = None
    config_folder_path = None
    exclude_file_extension = []
    application_details = {}
    application_name_keys = []
    process_to_terminate = []

    def __init__(self, app_setting, env_setting):
        self.env_setting = env_setting
        self.download_application_root_path = get_dict_value(env_setting, ["download_artifact_root_path"])
        self.config_folder_path = Folder.build_path(self.download_application_root_path,
                                                    get_dict_value(env_setting, ["artifact_config_folder"]))
        self.exclude_file_extension = get_dict_value(env_setting, ["exclude_file_extension"])

        self.process_to_terminate = get_dict_value(env_setting, ["windows_process_to_stop"])

        self.application_details = app_setting
        self.application_name_keys = app_setting.keys()

    def download_application(self):
        """ Download Applications """
        self.__get_and_update_download_list()
        download_instances = []
        for application in self.application_name_keys:
            download_instances.append(get_dict_value(self.application_details,
                                                     [application, "Download"]))  # type: DownloadApplication

        print self.spacer_char_asterisk
        map(self._start_thread, download_instances)
        map(self._join_thread, download_instances)
        # print "Completing {}, please wait".format(app_handler.application_name)
        print "\n" * DownloadApplication.application_count
        print self.spacer_char_hyphen
        map(self._print_download_info, download_instances)

    def _start_thread(self, instance):
        """
        start download thread
        @param instance: object of DowbloadApplication
        """
        application_instance = instance  # type: DownloadApplication
        application_instance.start()

    def _join_thread(self, instance):
        """
        join all thread of download
        @param instance: object of DowbloadApplication
        """
        application_instance = instance  # type: DownloadApplication
        application_instance.join()

    def _print_download_info(self, instance):
        """
        Print download status and information of application
        @param instance: object of DowbloadApplication
        """
        application_instance = instance  # type: DownloadApplication
        print "Application --> {}\n".format(application_instance.application_name)
        application_instance.print_download_status()
        application_instance.show_downloaded_info()

    def __get_and_update_download_list(self):
        """
        Download application
        @return: None
        """
        list_of_application_object = dict(
            map(self.__create_download_object, self.application_name_keys))
        for download_object in list_of_application_object:
            self.application_details[download_object]['Download'] = list_of_application_object[download_object]

    def __create_download_object(self, app_name):
        """
        Create download object
        @param app_name:
        @type app_name:
        @return:
        @rtype:
        """
        ignore_extensions = get_dict_value(self.env_setting, ["exclude_file_extension"])
        return app_name, DownloadApplication(app_name=app_name,
                                             download_artifact_root_path=self.download_application_root_path,
                                             exclude_file_extension=ignore_extensions)

    def get_application_details(self):
        return self.application_details
