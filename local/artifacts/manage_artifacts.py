from config.manage_json_config import get_dict_value
from infrastructure import configuration
from local.artifacts.download_application import DownloadApplication
from local.artifacts.replace_application import ReplaceApplication
from util import file_actions as File
from util import folder_actions as Folder

env_setting = configuration.get_environment_setting()


class ManageApplication:
    # self.path_to_vertexData = deployment_env_paths["path_vertexData"]
    # self.path_to_VertexApps = deployment_env_paths["path_vertexApp"]
    download_application_root_path = get_dict_value(env_setting, ["download_application_root_path"])
    config_folder_path = Folder.build_path(download_application_root_path,
                                           get_dict_value(env_setting, ["artifact_config_folder"]))
    exclude_file_extension = get_dict_value(env_setting, ["exclude_file_extension"])
    Folder.create_folder(download_application_root_path)
    Folder.create_folder(config_folder_path)

    application_details = {}
    application_name_keys = []

    def __init__(self, app_setting):
        self.application_details = app_setting
        self.application_name_keys = app_setting.keys()
        self.__make_app_handler_and_update()

    def _download_application(self):
        """ Download Applications """
        for application_handler in self.application_name_keys:
            self.application_details[application_handler]['Download'].start()
        for application_handler in self.application_name_keys:
            self.application_details[application_handler]['Download'].join()
        # extract config files
        map(self.__extract_configuration_file, self.application_name_keys)

    def __make_app_handler_and_update(self):
        list_of_application_object = dict(
            map(self.__create_app_download_handler, self.application_name_keys))  # type : DownloadApplication
        for app_object in list_of_application_object:
            self.application_details[app_object]['Download'] = list_of_application_object[app_object]

    def __create_app_download_handler(self, app_name):
        return app_name, DownloadApplication(download_artifact_root_path=self.download_application_root_path,
                                             folder_name=get_dict_value(self.application_details,
                                                                        [app_name, "folder_name"]),
                                             anchor_text=get_dict_value(self.application_details, [app_name, "anchor"]))

    def __TESTinit__(self, folder_name, config_file_name, find_text, replace_text, anchor_text):

        # self.folder_name = folder_name
        # self.config_file_name = config_file_name
        # self.find_text = find_text
        # self.replace_text = replace_text
        # self.anchor_text = anchor_text
        pass

    def __extract_configuration_file(self, app_name):
        # If config file name is supplied
        if Folder.folder_exists(self.config_folder_path):
            app_object = get_dict_value(self.application_details, [app_name, "Download"])
            config_file_name = get_dict_value(self.application_details, [app_name, "config_file_name"])
            if config_file_name:
                source_path = File.search_file_first_occurrence(filename=config_file_name,
                                                                search_path=app_object.download_path)
                if source_path:
                    save_to_path = Folder.build_path(self.config_folder_path, config_file_name)
                    File.copy_from_to_file(source=source_path, destination=save_to_path)
                    self.__replace_text_config_file_if_required(app_name=app_name, source_path=source_path)

    def __replace_text_config_file_if_required(self, app_name, source_path):
        # replace text only if required and size of both the list matches
        find_text = get_dict_value(self.application_details, [app_name, "find_text"])
        replace_text = get_dict_value(self.application_details, [app_name, "replace_text"])
        if find_text and replace_text and len(find_text) == len(replace_text):
            # better to search and replace via xpath, which has to be implemented
            File.find_replace_text_many(file_path=source_path, find_text_list=find_text,
                                        replace_text_list=replace_text)

    def __replace_old_application(self):
        # make list of applications to be replaced
        application_replace = {}
        config_replace = {}

        for application in self.application_name_keys:
            app_dest = get_dict_value(self.application_details, [application, "copy_artifacts_to_path"])
            if app_dest:
                app_handler = get_dict_value(self.application_details,
                                             [application, "Download"])  # type: DownloadApplication
                app_source = app_handler.download_path
                application_replace[application] = {'source': app_source, 'destination': app_dest}

            config_file_name = get_dict_value(self.application_details, [application, "config_file_name"])
            if config_file_name:
                config_source = Folder.build_path(self.config_folder_path, config_file_name)
                destinations = get_dict_value(self.application_details, [application, "copy_artifacts_to_path"])
                config_dest = []
                for destination in destinations:
                    config_dest.append(Folder.build_path(destination, config_file_name))
                    config_replace[application] = {'source': config_source, 'destination': config_dest}

        process_to_terminate = get_dict_value(env_setting, ["windows_process_to_stop"])
        application = ReplaceApplication(windows_process_to_stop=process_to_terminate,
                                                         application_replace_details=application_replace,
                                                         config_replace_details=config_replace)

        application.replace_applications()
