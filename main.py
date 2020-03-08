import os
from time import time
from datetime import datetime

from config_manager import ConfigManager
from framework_config import deployment_env_paths, local_database_setting
from local import setup_database as Database
from local.artifacts.manage_artifacts import ManageArtifacts
from util import file_actions as File
from util import folder_actions as Folder

spacer = '-' * 50


def write_to_file_setup_info(to_file, artifacts=None, sql_path=None, test_mode=0):
    File.append_text_to_file(to_file, spacer, "\n", spacer)
    File.append_text_to_file(to_file, "\t\tApp version(s) TeamCity\n")
    sql_version = None
    if test_mode == 0:
        write_downloaded_application_version_info(file_path=to_file, artifact=artifacts)
        sql_version = (lambda value: artifacts.application.service.build_version_number if
        artifacts.application.service.build_version_number else None)(artifacts.application.service.build_version_number)
    elif test_mode != 0:
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
                                     artifact.application.dataservice.build_id)
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <DataService>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.reports.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.reports.folder, "\t\t\t\t",
                                     artifact.application.reports.build_id)
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Reports>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.service.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.service.folder, "\t\t\t\t",
                                     artifact.application.service.build_id)
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Service>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.shell.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.shell.folder, "\t\t\t\t",
                                     artifact.application.shell.build_id)
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <Shell>: {}\nargs{}".format(err.message, err.args)
    try:
        if artifact.application.ui.compare_file_count():
            File.append_text_to_file(file_path, "\t", artifact.application.ui.folder, "\t\t\t\t",
                                     artifact.application.ui.build_id)
    except (AttributeError, ValueError, TypeError) as err:
        print "Error in writing version info <UI>: {}\nargs{}".format(err.message, err.args)


def write_dummy_info_to_file(file_path):
    File.append_text_to_file(file_path, "\tF1", "\t\t\t\t", "123")
    File.append_text_to_file(file_path, "\tF2", "\t\t\t\t", "123")
    File.append_text_to_file(file_path, "\tF3", "\t\t\t\t", "321")


def artifact_download(test_mode):
    # Folder.delete_folder_contents(deployment_env_paths["path_download_root"])
    file_version_txt = Folder.build_path(deployment_env_paths["path_download_root"], 'AppVersion_downloaded.txt')

    artifact = ManageArtifacts()
    # Download all artifacts
    artifact.download_artifacts()
    # Replace old with new artifacts
    artifact.replace_artifacts()

    sql_path = os.path.join(deployment_env_paths["path_download_root"], local_database_setting["db_to_setup"])
    if File.file_exists(sql_path):
        Database.recreate_database_from_script(sql_path)

    if artifact.application and sql_path and test_mode != 0:
        write_to_file_setup_info(to_file=file_version_txt, artifacts=artifact, sql_path=sql_path, test_mode=test_mode)
    else:
        write_to_file_setup_info(to_file=file_version_txt, test_mode=test_mode)


def artifact_download_with_timer(test_mode):
    # Folder.delete_folder_contents(deployment_env_paths["path_download_root"])
    file_version_txt = Folder.build_path(deployment_env_paths["path_download_root"], 'AppVersion_downloaded.txt',
                                         datetime.now().strftime("%d%m%Y_%H%M%S"))
    start_s = time()
    start_time = datetime.now().strftime("%H:%M:%S")
    File.delete_file(file_version_txt)
    time_db = None

    artifact = ManageArtifacts()

    # Download all artifacts
    start = time()
    artifact.download_artifacts()
    end = time()
    time_download = end - start

    # Replace old with new artifacts
    start = time()
    artifact.replace_artifacts()
    end = time()
    time_replace = end - start

    sql_path = os.path.join(deployment_env_paths["path_download_root"], local_database_setting["db_to_setup"])
    if File.file_exists(sql_path):
        start = time()
        Database.recreate_database_from_script(sql_path)
        end = time()
        time_db = end - start
        write_to_file_setup_info(to_file=file_version_txt, artifacts=artifact, sql_path=sql_path, test_mode=test_mode)

    print "{}\n{}".format('#' * 45, '  *' * 15)
    print "Artifact download time: {}".format(get_time(time_download))
    print "Artifact replacement time: {}".format(get_time(time_replace))
    print "Database re-create time: {}".format(get_time(time_db))
    print "{}\n{}".format("  *" * 15, "#" * 45)

    File.append_text_to_file(file_version_txt, spacer, "\n", spacer)
    File.append_text_to_file(file_version_txt, "\t\tTimings (hh:mm:ss)\n")
    File.append_text_to_file(file_version_txt, "Download build -----> {}", get_time(time_download))
    File.append_text_to_file(file_version_txt, "Replace build  -----> {}", get_time(time_replace))
    File.append_text_to_file(file_version_txt, "Database recreate --> {}", get_time(time_db))
    end_s = time()
    end_time = datetime.now().strftime("%H:%M:%S")
    time_s = end_s - start_s
    File.append_text_to_file(file_version_txt, "Total execution ----> {}", get_time(time_s))
    File.append_text_to_file(file_version_txt, spacer, "\n", spacer)

    File.append_text_to_file(file_version_txt, "\t\tScript (hh:mm:ss)\n")
    File.append_text_to_file(file_version_txt, "Start --> {}", start_time)
    File.append_text_to_file(file_version_txt, "End --> {}", end_time)
    File.append_text_to_file(file_version_txt, spacer, "\n", spacer)


def get_time(float_time):
    hours, rem = divmod(float_time, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def check_infra():
    configuration = ConfigManager()

    if configuration.update_framework_config():
        print "Configuration files: Ok"
        # if configuration.check_connection():
        #     print "TeamCity server: Ok"
        # else:
        #     print "TeamCity server: Bad"
        #     exit(0)
    else:
        print "Configuration files: Bad"
        exit(0)


def main(test_mode=0):
    print check_infra()
    print artifact_download_with_timer(test_mode)
    # write_to_file_setup_info(artifacts=None, sql_path=r"C:\DEMO_TeamCity\Artifacts\SQL\Vertex_and_Games_on_VertexBox.sql")


if __name__ == '__main__':
    main(0)
