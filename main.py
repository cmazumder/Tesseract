import sys

try:
    from config.framework_config import Environment
except (ImportError, Environment) as err:
    print "Error: {}\nMissing framkework_config.py, recreating now".format(err.message)

from config import framework_config_PROD, framework_config_TEST
from setup import controller_infrastructure_ready, start_controller_setup
import util.file_actions as File
import util.folder_actions as Folder


def config_file_select(test_mode):
    destination_path = Folder.build_path("config/", 'framework_config.py')
    if test_mode:
        source_path = Folder.build_path("config/", 'framework_config_TEST.py')
        if not File.file_exists(destination_path):
            File.copy_from_to_file(source=source_path, destination=destination_path)
        else:
            if Environment.lower() != framework_config_TEST.Environment.lower():
                File.copy_from_to_file(source=source_path, destination=destination_path)
    else:
        source_path = Folder.build_path("config/", 'framework_config_PROD.py')
        if not File.file_exists(destination_path):
            File.copy_from_to_file(source=source_path, destination=destination_path)
        else:
            if Environment.lower() != framework_config_PROD.Environment.lower():
                File.copy_from_to_file(source=source_path, destination=destination_path)


def main(test_mode=False):
    config_file_select(test_mode)
    if controller_infrastructure_ready():
        start_controller_setup(test_mode)
    else:
        sys.exit("Issue with infrastructure")


if __name__ == '__main__':
    main(test_mode=False)
