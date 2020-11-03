"""
Simple text output to a log file about task performed and version information of application(s)
"""

from time import time, localtime, strftime

from ConfigManager.ManageJsonConfig import get_dict_value
from local.artifacts.DownloadApplication import DownloadApplication
from local.artifacts.ReplaceApplication import ReplaceApplication
from util import FileActions as File
from util import FolderActions as Folder


class DeploymentLog:
    """
    Class to manage log output file and write information to it

    Tasks: Create file, write application version information. Download and replacement status.
    Database setup script used and time for each activity
    """
    spacer = '-' * 63
    filename = None
    log_file = None
    artifact_details = {}
    app_keys = []
    center_align = "{:^50s}"
    center_align_filler = "{:*^50s}"
    tab_text = "{:15s}"

    def __init__(self, file_path):
        self.filename = "BuildDeploymentInfo_" + strftime("%Y-%m-%dT%H%M%S", localtime()) + ".log"
        self.start_time_formatted = strftime("%H:%M:%S", localtime())  # The execution local start time
        self.start_time = self.time_it()
        self.log_file = Folder.build_path(file_path, self.filename)

    def time_it(self):
        """
        Return the time in seconds since the epoch as a floating point number

        :return: time in seconds
        :rtype: float
        """
        return time()

    def _get_readable_epoch_time(self, float_time, hour=False):
        """
        Convert epoch time to human readable format

        :param float_time: time in sec
        :type float_time: float
        :param hour: If need HH:MM:SS format
        :type hour: bool
        :return: timestamp
        :rtype: str
        """
        hours, rem = divmod(float_time, 3600)
        minutes, seconds = divmod(rem, 60)
        if not hour:
            return "{:0>2}:{:05.2f}".format(int(minutes), seconds)
        else:
            return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

    def set_artifact_details(self, app_details):
        """
        Set artifact details

        :param app_details: details of all artifacts that has been downloaded
        :type app_details: dict
        """
        self.artifact_details = app_details
        self.app_keys = self.artifact_details.keys()
        self.app_keys.sort()

    def elapsed_time(self, start, end):
        """
        Calculate the elapsed time between start and end

        :param start: start time
        :type start: float
        :param end: end time
        :type end: float
        :return: timestamp
        :rtype: str
        """
        return self._get_readable_epoch_time(float_time=end - start)

    def _write_app_version_info(self, application_key):
        app_download = get_dict_value(self.artifact_details, [application_key, "Download"])  # type: DownloadApplication
        app_copy = get_dict_value(self.artifact_details, [application_key, "Replace"])  # type: ReplaceApplication
        
        try:
            app_version = app_download.get_version_number()
            app_download_status = "Success" if (app_download.get_download_status()) else "Failure"
        except (TypeError, AttributeError):
            print "Download status not present for {}".format(application_key)
            app_version = 'None'
            app_download_status = 'None'
            
        try:
            app_copy_status = "Success" if (app_copy.get_replace_status()) else "Failure"
        except (TypeError, AttributeError):
            print "Copy status not present for {}".format(application_key)
            app_copy_status = 'NA'
            
        string = ("\t" + self.tab_text * 4).format(str(application_key), str(app_version), str(app_download_status),
                                                   str(app_copy_status))
        File.append_text_to_file(self.log_file, string)
        print string

    def write_deployment_status(self, app_details=None):
        """
        Write deployment status of each artifact to file

        :param app_details: details of all artifacts that has been downloaded
        :type app_details: dict
        """
        File.append_text_to_file(self.log_file, self.spacer)
        string = self.center_align_filler.format(" Application information ")
        File.append_text_to_file(self.log_file, string, "\n")
        self.set_artifact_details(app_details=app_details)

        if self.app_keys:
            string = ("\t" + self.tab_text * 8).format("App", "Version", "Download", "Replace\n", "", "",
                                                       "status", "status")
            File.append_text_to_file(self.log_file, string, "\n")
            print "{}\n{}".format("  *" * 20, "#" * 58)
            print string
            map(self._write_app_version_info, self.app_keys)
            print "{}\n{}".format("  *" * 20, "#" * 58)

    def write_database_info(self, script_name):
        """
        Write database script information to file

        :param script_name: name of the db script
        :type script_name: str
        """
        File.append_text_to_file(self.log_file, self.spacer)
        string = self.center_align_filler.format(" Database information ")
        File.append_text_to_file(self.log_file, string, "\n")
        string = ("\t" + self.tab_text * 2).format("Script:", str(script_name))
        File.append_text_to_file(self.log_file, string)
        string = ("\t" + self.tab_text * 2).format("Status:", "Recreated")
        File.append_text_to_file(self.log_file, string)

    def write_artifact_info(self, download_path):
        """
        Write information related to every artifacts. Such as folder size, number of files
        along with the download and replacement status of each artifact to file

        :param download_path: root path of downloaded artifacts
        :type download_path: str
        """
        if self.app_keys:
            File.append_text_to_file(self.log_file, self.spacer)
            string = self.center_align_filler.format(" Artifact information ")
            File.append_text_to_file(self.log_file, string, "\n")
            string = ("\t" + self.tab_text * 2).format("Location:", str(download_path))
            File.append_text_to_file(self.log_file, string)
            string = ("\t" + self.tab_text * 2).format("Folder(s):", str(len(self.app_keys)))
            File.append_text_to_file(self.log_file, string, "\n")
            string = ("\t" + self.tab_text * 10).format("FolderName", "Download", "Replace", "Downloaded",
                                                        "Replaced\n", "", "size", "size", "file(s)", "file(s)")
            File.append_text_to_file(self.log_file, string, "\n")
            map(self._write_folder_property, self.app_keys)

    def _write_folder_property(self, application_key):
        app_download = get_dict_value(self.artifact_details, [application_key, "Download"])  # type: DownloadApplication
        app_copy = get_dict_value(self.artifact_details, [application_key, "Replace"])  # type: ReplaceApplication
        app_folder_name = get_dict_value(self.artifact_details, [application_key, "folder_name"]) \
            if get_dict_value(self.artifact_details, [application_key, "folder_name"]) else application_key
        try:
            download_files, fld, download_size = Folder.get_folder_properties(app_download.get_download_folder())
            download_size = Folder.convert_bytes(download_size)
        except (TypeError, AttributeError):
            print "Could not download: {}".format(application_key)
            download_size = 'NA'
            download_files = 'NA'
        try:
            copy_files, fld, copy_size = Folder.get_folder_properties(app_copy.get_replace_folder()[0])
            copy_size = Folder.convert_bytes(copy_size)
        except (TypeError, AttributeError):
            print "Could not copy: {}".format(application_key)
            copy_size = 'NA'
            copy_files = 'NA'

        string = ("\t" + self.tab_text * 5).format(str(app_folder_name), str(download_size), str(copy_size),
                                                   str(download_files), str(copy_files))
        File.append_text_to_file(self.log_file, string)

    def write_time(self, time_download=None, time_replace=None, time_db=None):
        """
        Write elapsed time of activities to file
        """
        File.append_text_to_file(self.log_file, self.spacer)
        string = self.center_align_filler.format(" Total elapsed time (mm:ss) ")
        File.append_text_to_file(self.log_file, string, "\n")
        if time_download:
            string = ("\t" + self.tab_text * 2).format("Download -->", str(time_download))
            File.append_text_to_file(self.log_file, string)
        if time_replace:
            string = ("\t" + self.tab_text * 2).format("Replace -->", str(time_replace))
            File.append_text_to_file(self.log_file, string)
        if time_db:
            string = ("\t" + self.tab_text * 2).format("Database -->", str(time_db))
            File.append_text_to_file(self.log_file, string)

        end_time_formatted = strftime("%H:%M:%S", localtime())  # The execution local start time
        total_elapsed_time = self._get_readable_epoch_time(float_time=self.time_it() - self.start_time)
        string = ("\t" + self.tab_text * 2).format("Execution --> ", total_elapsed_time)
        File.append_text_to_file(self.log_file, string)

        # print local time of program execution
        File.append_text_to_file(self.log_file, self.spacer)
        string = self.center_align_filler.format(" Clock (local time) ")
        File.append_text_to_file(self.log_file, string, "\n")
        string = ("\t" + self.tab_text * 2).format("Start --> ", self.start_time_formatted)
        File.append_text_to_file(self.log_file, string)
        string = ("\t" + self.tab_text * 2).format("End   --> ", end_time_formatted)
        File.append_text_to_file(self.log_file, string)
        File.append_text_to_file(self.log_file, self.spacer)
