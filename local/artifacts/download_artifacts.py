from util import file_actions as File, folder_actions as Folder
from vertex.dataservice import DataService
from vertex.reports import Reports
from vertex.service import Service
from vertex.shell import Shell
from vertex.userinterface import UI


class DownloadArtifacts:
    spacer = '-' * 50

    def __init__(self):
        self.config_download_path = Folder.build_path(deployment_env_paths["path_download_root"],
                                                      deployment_env_paths["config_folder"])
        self.shell = self.ui = self.dataservice = self.reports = self.service = None
        pass

    def download_applications(self):

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

    def extract_configuration_files(self, search_in_path, save_to_path, file_name):
        if Folder.folder_exists(save_to_path):
            source_path = File.search_file_first_occurrence(filename=file_name, search_path=search_in_path)
            if source_path:
                save_to_path = Folder.build_path(save_to_path, file_name)
                if 'Shell.config' in file_name:
                    # better to search and replace via xpath, which has to be implemented
                    File.find_replace_text(source_path, r'enabled="true"', r'enabled="false"')
            File.copy_from_to_file(source=source_path, destination=save_to_path)

    def download(self):
        if Folder.create_folder(self.config_download_path):
            self.download_applications()

            if self.service.compare_file_count():
                self.extract_configuration_files(search_in_path=self.service.artifact_download_path,
                                                 save_to_path=self.config_download_path,
                                                 file_name=application_structure["service"]["config_file_name"])

            if self.dataservice.compare_file_count():
                self.extract_configuration_files(search_in_path=self.dataservice.artifact_download_path,
                                                 save_to_path=self.config_download_path,
                                                 file_name=application_structure["dataservice"]["config_file_name"])

            if self.reports.compare_file_count():
                self.extract_configuration_files(search_in_path=self.reports.artifact_download_path,
                                                 save_to_path=self.config_download_path,
                                                 file_name=application_structure["reports"]["config_file_name"])

            if self.shell.compare_file_count():
                self.extract_configuration_files(search_in_path=self.shell.artifact_download_path,
                                                 save_to_path=self.config_download_path,
                                                 file_name=application_structure["shell"]["config_file_name"])

            if self.ui.compare_file_count():
                self.extract_configuration_files(search_in_path=self.ui.artifact_download_path,
                                                 save_to_path=self.config_download_path,
                                                 file_name=application_structure["ui"]["config_file_name"])
