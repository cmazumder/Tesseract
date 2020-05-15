import time

from config.manage_json_config import get_dict_value
from util import file_actions as File
from util import folder_actions as Folder
from util import os_process


class ReplaceApplication:
    """
    Take care of replacement of binaries of applications
    """
    """
    application_replace_details - will save the information of the applications to be replaced
    AppName : {
                source: 'path',
                destination: [list of folder],
                status: True/False
                }
    """
    application_replace_details = {}
    application_name_keys = []
    """
    config_replace_details - will save the information of the configs that are to be replaced
    AppName : {
                source: 'path',
                destination: [list of folder],
                status: True/False
                }
    """
    config_replace_details = {}
    config_name_keys = []
    process_to_terminate = []

    def __init__(self, windows_process_to_stop, application_replace_details, config_replace_details):
        if windows_process_to_stop and type(windows_process_to_stop) is list:
            self.process_to_terminate = windows_process_to_stop
        # set applications details
        if application_replace_details and type(application_replace_details) is dict:

            self.application_replace_details = application_replace_details
            self.application_name_keys = self.application_replace_details.keys()
            for item in self.application_name_keys:
                if not get_dict_value(self.application_replace_details, [item, "destination"]):
                    try:
                        del self.application_replace_details[item]
                        self.application_name_keys.remove(item)
                    except KeyError as err:
                        print "Key error: {}".format(err.message)

        # set config file details
        if config_replace_details and type(config_replace_details) is dict:
            self.config_replace_details = config_replace_details
            self.config_name_keys = self.config_replace_details.keys()
            for item in self.config_replace_details:
                if not get_dict_value(self.config_replace_details, [item, "destination"]):
                    try:
                        del self.config_replace_details[item]
                        self.config_name_keys.remove(item)
                    except KeyError as err:
                        print "Key error: {}".format(err.message)


    def __close_running_process(self, process_name):
        # process_detail = get_processid_by_name('chrome', 'conhost', 'pycharm64.exe', 'WinMergeU')
        try:
            process_detail = os_process.get_processid_by_name(process_name=process_name)
            if len(process_detail) > 0:
                for element in process_detail:
                    curr_pid = element['pid']
                    curr_name = element['name']
                    curr_created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(element['create_time']))
                    print curr_pid, curr_name, curr_created_time
                    status = os_process.kill_process_tree(pid=curr_pid)
                    print "Process: {0}\tpid: {1}\tStatus:{2}".format(process_name, curr_pid, status)
            else:
                print"No running process found: {}".format(process_name)
        except (ValueError, TypeError, AttributeError) as err:
            print "Error closing process: {}\nargs:".format(err.message, err.args)

    def __copy_application(self, applicataion_name):
        status = True
        source = self.application_replace_details[applicataion_name]['source']
        destinations = self.application_replace_details[applicataion_name]['destination']
        for destination in destinations:
            Folder.copy_from_to_location(source=source, destination=destination)
            if not self.__check_folder_copy_status(source=source, destination=destination):
                status = False
        self.application_replace_details[applicataion_name]['status'] = status

    def __check_folder_copy_status(self, source, destination):
        source_folder_property = Folder.get_folder_properties(source)
        destination_folder_property = Folder.get_folder_properties(destination)
        # compare between source and dest the count of files, sub folders and size
        if source_folder_property[0] == destination_folder_property[0] and \
                source_folder_property[0] == destination_folder_property[0] and \
                source_folder_property[0] == destination_folder_property[0]:
            return True
        else:
            return False

    def __copy_config_file(self, config_name):
        status = True
        source = self.config_replace_details[config_name]['source']
        destinations = self.config_replace_details[config_name]['destination']
        for destination in destinations:
            File.copy_from_to_file(source=source, destination=destination)
            if not self.__check_file_copy_status(source=source, destination=destination):
                status = False
        self.config_replace_details[config_name]['status'] = status

    def __check_file_copy_status(self, source, destination):
        source_file_size = File.compute_file_size(source)
        destination_file_size = File.compute_file_size(destination)
        # compare source and dest file size
        if source_file_size == destination_file_size:
            return True
        else:
            return False

    def replace_applications(self):
        map(self.__close_running_process, self.process_to_terminate)
        map(self.__copy_application, self.application_name_keys)
        map(self.__copy_config_file, self.config_name_keys)

    def get_application_replace_status(self):
        return self.application_replace_details

    def get_config_replace_details(self):
        return self.config_replace_details
