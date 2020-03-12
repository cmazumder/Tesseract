import sys
from make_configuration import controller_infrastructure_ready, start_controller_setup
try:
    from config.framework_config import Environment, process_to_stop
except (ImportError, Environment) as err:
    print "Error: {}\nMissing framework_config.py, recreate".format(err.message)
import util.file_actions as File
import util.folder_actions as Folder


def config_file_select(test_mode):
    destination_path = Folder.build_path("config/", 'framework_config.py')
    if test_mode:
        source_path = Folder.build_path("config/", 'framework_config_TEST.py')
        File.copy_from_to_file(source=source_path, destination=destination_path)
    else:
        source_path = Folder.build_path("config/", 'framework_config_PROD.py')
        File.copy_from_to_file(source=source_path, destination=destination_path)
    print "Run: {}\nProcess: {}".format(Environment, process_to_stop)


def main(test_mode=False):
    config_file_select(test_mode)
    if controller_infrastructure_ready():
        start_controller_setup(test_mode)
    else:
        sys.exit("Issue with infrastructure")


if __name__ == '__main__':
    main(test_mode=False)