import time
from os import listdir

from local.artifacts.download import Download
from util import file_actions as File
from util import folder_actions as Folder
from util import os_process


class ManageArtifacts:
    def __init__(self):
        try:
            self.application = Download()
            self.path_to_vertexData = deployment_env_paths["path_vertexData"]
            self.path_to_VertexApps = deployment_env_paths["path_vertexApp"]
        except (KeyError, NameError) as err:
            print "Error: {0}\nArgs: {1}".format(err.message, err.args)

    def download_artifacts(self):
        """
        Download artifacts
        :return:
        :rtype:
        """
        self.application.download()
        print "Downloaded"


    def extract_configuration_files(self, search_in_path, save_to_path, file_name):
        if Folder.folder_exists(save_to_path):
            source_path = File.search_file_first_occurrence(filename=file_name, search_path=search_in_path)
            if source_path:
                save_to_path = Folder.build_path(save_to_path, file_name)
                if 'Shell.config' in file_name:
                    # better to search and replace via xpath, which has to be implemented
                    File.find_replace_text(source_path, r'enabled="true"', r'enabled="false"')
            File.copy_from_to_file(source=source_path, destination=save_to_path)

    def close_running_process(self):
        # process_ids = get_processid_by_name('chrome', 'conhost', 'pycharm64.exe', 'WinMergeU')
        try:
            for item in environment_setting:
                process_ids = os_process.get_processid_by_name(item)
                if len(process_ids) > 0:
                    for elem in process_ids:
                        processID = elem['pid']
                        processName = elem['name']
                        processCreationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
                        # processCreationTime = elem['create_time']
                        print processID, processName, processCreationTime
                        status = os_process.kill_process_tree(pid=processID)
                        print "Process: {0}\tpid: {1}\tStatus:{2}".format(processName, processID, status)
                else:
                    print"No running process found: {}".format(item)
        except (ValueError, TypeError, AttributeError) as err:
            print "Error closing process: {}\nargs:".format(err.message, err.args)

    def replace_old_builds(self):
        """

        :return:
        :rtype:
        """
        if self.application.service and self.application.service._count_of_download_and_artifact_list_match():
            self.copy_artifact(self.application.service)
        if self.application.shell and self.application.shell._count_of_download_and_artifact_list_match():
            self.copy_artifact(self.application.shell)
        if self.application.ui and self.application.ui._count_of_download_and_artifact_list_match():
            self.copy_artifact(self.application.ui)
        if self.application.dataservice and self.application.dataservice._count_of_download_and_artifact_list_match():
            self.copy_artifact(self.application.dataservice)
        if self.application.reports and self.application.reports._count_of_download_and_artifact_list_match():
            self.copy_artifact(self.application.reports)

    def copy_artifact(self, application):
        """
        Use only with object of application downloaded
        :param application:
        :type application:
        :return: None
        """
        destination_path = Folder.build_path(self.path_to_VertexApps, application.Folder)
        Folder.copy_from_to_location(source=application.artifact_download_path, destination=destination_path)

    def replace_configuration_file(self):
        source_path = r''
        path_to_VertexData = Folder.build_path(self.path_to_vertexData, deployment_env_paths["config_folder"])
        path_to_VertexApps = Folder.build_path(self.path_to_VertexApps, deployment_env_paths["backup_folder"],
                                               deployment_env_paths["config_folder"])

        if Folder.create_folder(path_to_VertexData) and Folder.create_folder(path_to_VertexApps):
            try:
                for file in listdir(self.application.config_download_path):
                    source_path = Folder.build_path(self.application.config_download_path, file)
                    if File.file_exists(source_path):
                        # copy to F configuration
                        File.copy_from_to_file(source=source_path, destination=path_to_VertexData)
                        # copy to D configuration
                        File.copy_from_to_file(source=source_path, destination=path_to_VertexApps)
            except WindowsError as err:
                print "File or Folder not available: {} \nargs: {}".format(err.message, err.args)

    def replace_artifacts(self):
        self.close_running_process()
        self.replace_old_builds()
        self.replace_configuration_file()
