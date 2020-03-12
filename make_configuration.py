import os
from time import time, localtime, strftime

from config.config_manager import ConfigManager
from config.framework_config import deployment_env_paths, local_database_setting
from local import setup_database as Database
from local.artifacts.manage_artifacts import ManageArtifacts
from util import file_actions as File
from util import folder_actions as Folder

spacer = '-' * 50


def write_to_file_setup_info(to_file, artifacts=None, sql_path=None, test_mode=False):
    File.append_text_to_file(to_file, spacer, "\n", spacer)
    File.append_text_to_file(to_file, "\t\tApp version(s) TeamCity\n")
    sql_version = None
    if not test_mode:
        write_downloaded_application_version_info(file_path=to_file, artifact=artifacts)
        sql_version = (lambda value: artifacts.application.service.version_number if
        artifacts.application.service.version_number else None)(artifacts.application.service.version_number)
    elif test_mode:
        sql_version = "Test.2.2"
        write_dummy_info_to_file(to_file)

    File.append_text_to_file(to_file, spacer, "\n", spacer)

    File.append_text_to_file(to_file, "\t\tDownloaded new apps\n")
    File.append_text_to_file(to_file, "\tLocation: ", deployment_env_paths["path_download_root"])
    File.append_text_to_file(to_file, spacer, "\n", spacer)

    File.append_text_to_file(to_file, "\t\tReplaced old apps\n")
    File.append_text_to_file(to_file, "\tLocation: ", deployment_env_paths["path_vertexApp"])
    File.append_text_to_file(to_file, spacer, "\n", spacer)

    if sql_path:
        File.append_text_to_file(to_file, "\t\tDatabase\n")
        File.append_text_to_file(to_file, "\tScript: ", File.path.basename(sql_path))
        File.append_text_to_file(to_file, "\tService #: ", sql_version)
        File.append_text_to_file(to_file, "\tStatus: Re-created with latest")
        File.append_text_to_file(to_file, spacer, "\n", spacer)


def write_downloaded_application_version_info(file_path, artifact):
    try:
        if artifact.application.dataservice.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.dataservice.folder, "\t\t\t",
                                     artifact.application.dataservice.version_number)
        else:
            File.append_text_to_file(file_path, "\t", artifact.application.dataservice.folder, "\t\t\t",
                                     "NA")
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <DataService>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.reports.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.reports.folder, "\t\t\t\t",
                                     artifact.application.reports.version_number)
        else:
            File.append_text_to_file(file_path, "\t", artifact.application.reports.folder, "\t\t\t",
                                     "NA")
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Reports>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.service.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.service.folder, "\t\t\t\t",
                                     artifact.application.service.version_number)
        else:
            File.append_text_to_file(file_path, "\t", artifact.application.service.folder, "\t\t\t",
                                     "NA")
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Service>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.shell.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.shell.folder, "\t\t\t\t",
                                     artifact.application.shell.version_number)
        else:
            File.append_text_to_file(file_path, "\t", artifact.application.shell.folder, "\t\t\t",
                                     "NA")
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Shell>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.ui.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.ui.folder, "\t\t\t\t\t",
                                     artifact.application.ui.version_number)
        else:
            File.append_text_to_file(file_path, "\t", artifact.application.ui.folder, "\t\t\t",
                                     "NA")
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <UI>: {}\nargs{}".format(err.message, err.args)


def write_dummy_info_to_file(file_path):
    File.append_text_to_file(file_path, "\tF1", "\t\t\t\t", "123")
    File.append_text_to_file(file_path, "\tF2", "\t\t\t\t", "123")
    File.append_text_to_file(file_path, "\tF3", "\t\t\t\t", "321")


def start_controller_setup(test_mode):
    file_name = "BuildDeploymentInfo_" + strftime("%Y-%m-%dT%H%M%S", localtime()) + ".txt"
    # File to save the stats such as apps downloaded and their version, db script used and etc
    file_save_deployment_stats = Folder.build_path(deployment_env_paths["path_download_root"], file_name)

    start_s = time()  # The execution epoch start time
    start_time = strftime("%H:%M:%S", localtime())  # The execution local start time

    artifact = ManageArtifacts()

    # Download all artifacts
    start = time()  # Download epoch start time
    artifact.download_artifacts()
    end = time()  # Download epoch finish time
    time_download = end - start

    # Replace old with new artifacts
    start = time()  # Build replacement epoch start time
    artifact.replace_artifacts()
    end = time()  # Build replacement epoch start time
    time_replace = end - start

    sql_path = os.path.join(deployment_env_paths["path_download_root"], local_database_setting["db_to_setup"])
    time_db = None
    if File.file_exists(sql_path):
        start = time()  # Download epoch start time
        Database.recreate_database_from_script(sql_path)
        end = time()  # Download epoch start time
        time_db = end - start
        write_to_file_setup_info(to_file=file_save_deployment_stats, artifacts=artifact, sql_path=sql_path,
                                 test_mode=test_mode)

    print "{}\n{}".format('#' * 45, '  *' * 15)
    print "Artifact download time: {}".format(get_readable_epoch_time(time_download))
    print "Artifact replacement time: {}".format(get_readable_epoch_time(time_replace))
    print "Database re-create time: {}".format(get_readable_epoch_time(time_db))
    print "{}\n{}".format("  *" * 15, "#" * 45)

    File.append_text_to_file(file_save_deployment_stats, "\t\tElapsed time (hh:mm:ss)\n")
    File.append_text_to_file(file_save_deployment_stats, "\tDownload build -----> ",
                             get_readable_epoch_time(time_download))
    File.append_text_to_file(file_save_deployment_stats, "\tReplace build  -----> ",
                             get_readable_epoch_time(time_replace))
    File.append_text_to_file(file_save_deployment_stats, "\tDatabase recreate --> ", get_readable_epoch_time(time_db))
    end_s = time()
    time_s = end_s - start_s
    File.append_text_to_file(file_save_deployment_stats, "\tTotal execution ----> ", get_readable_epoch_time(time_s))
    File.append_text_to_file(file_save_deployment_stats, spacer, "\n", spacer)

    File.append_text_to_file(file_save_deployment_stats, "\t\tTime (local time)\n")
    File.append_text_to_file(file_save_deployment_stats, "\tStart --> ", start_time)
    end_time = strftime("%H:%M:%S", localtime())
    File.append_text_to_file(file_save_deployment_stats, "\tEnd ----> ", end_time)
    File.append_text_to_file(file_save_deployment_stats, spacer, "\n", spacer)


def get_readable_epoch_time(float_time):
    hours, rem = divmod(float_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def check_database_connection():
    database = Database.get_database_connection()
    if database.connection:
        return True
    else:
        return False


def controller_infrastructure_ready():
    configuration = ConfigManager()
    status = True
    if configuration.update_framework_config():
        print "Configuration files: Ok"
    else:
        print "Configuration files: Bad"
        status = False
    if configuration.check_teamcity_available():
        print "TeamCity server: Ok"
    else:
        print "TeamCity server: Bad"
        status = False
    if check_database_connection():
        print "Database server: Ok"
    else:
        print "Database server: Bad"
        status = False
    return status
