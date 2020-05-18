from time import time, localtime, strftime

from local.artifacts.download_application import DownloadApplication
from local.artifacts.replace_application import ReplaceApplication
from util import file_actions as File
from util import folder_actions as Folder


class DeploymentLog:
    spacer = '-' * 50
    filename = None
    log_file = None
    artifact_details = {}
    app_keys = []

    def __init__(self, file_path):
        self.filename = "BuildDeploymentInfo_" + strftime("%Y-%m-%dT%H%M%S", localtime()) + ".log"
        self.start_time_formatted = strftime("%H:%M:%S", localtime())  # The execution local start time
        self.start_time = self.time_it()
        self.log_file = Folder.build_path(file_path, self.filename)

    def time_it(self):
        return time()

    def _get_readable_epoch_time(self, float_time, hour=False):
        hours, rem = divmod(float_time, 3600)
        minutes, seconds = divmod(rem, 60)
        if not hour:
            return "{:0>2}:{:05.2f}".format(int(minutes), seconds)
        else:
            return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

    def set_artifact_details(self, app_detail):
        self.artifact_details = app_detail
        self.app_keys = self.artifact_details.key()

    def total_time(self, start, end):
        return self._get_readable_epoch_time(float_time=start - end)

    def _write_app_version_info(self, artifact_download):
        app_download = artifact_download  # type: DownloadApplication
        app_copy = artifact_download  # type: ReplaceApplication
        File.append_text_to_file(self.log_file, "\t", app_download.application_name, "\t\t\t",
                                 app_download.version_number, "\t", app_download.get_download_status(), "\t",
                                 app_copy.get_replace_status())

    def write_deployment_status(self, app_details=None):
        File.append_text_to_file(self.log_file, self.spacer, "\n", self.spacer)
        File.append_text_to_file(self.log_file, "\t\tApplication information\n")
        sql_version = None

        self.set_artifact_details(app_detail=app_details)

        if self.app_keys:
            File.append_text_to_file(self.log_file, "\t", "Name", "\t\t\t", "Version", "\t", "Download Status:", "\t",
                                     "Copy Status")
            map(self._write_app_version_info, self.app_keys)

        File.append_text_to_file(self.log_file, self.spacer, "\n", self.spacer)

    def write_time(self, time_download=None, time_replace=None, time_db=None):
        print "{}\n{}".format('#' * 45, '  *' * 15)
        File.append_text_to_file(self.log_file, "\t\tElapsed time (mm:ss)\n")

        if time_download:
            print "Artifact download time: {}".format(time_download)
            File.append_text_to_file(self.log_file, "\tDownloadApplication build -----> ", time_download)
        if time_replace:
            print "Artifact replacement time: {}".format(time_replace)
            File.append_text_to_file(self.log_file, "\tReplace build  -----> ", time_replace)
        if time_db:
            print "Database re-create time: {}".format(time_db)
            File.append_text_to_file(self.log_file, "\tDatabase recreate --> ", time_db)
        print "{}\n{}".format("  *" * 15, "#" * 45)

        end_time_formatted = strftime("%H:%M:%S", localtime())  # The execution local start time
        total_elapsed_time = self._get_readable_epoch_time(float_time=self.start_time - self.time_it())

        File.append_text_to_file(self.log_file, "\tTotal execution ----> ", total_elapsed_time)
        File.append_text_to_file(self.log_file, self.spacer, "\n", self.spacer)
        File.append_text_to_file(self.log_file, "\t\tTime (local time)\n")
        File.append_text_to_file(self.log_file, "\tStart --> ", self.start_time_formatted)
        File.append_text_to_file(self.log_file, "\tEnd ----> ", end_time_formatted)
        File.append_text_to_file(self.log_file, self.spacer, "\n", self.spacer)
