import sys

from Infrastructure import Infrastructure
from config.config_manager import ConfigManager


def main(test_mode=False):
    if test_mode == 'v':
        print "TEST MODE VERTEX"
        config_file_path = r"json_config/test_config/config_path_TEST_VERTEX.json"
    elif test_mode == 'n':
        print "TEST MODE NABLER"
        config_file_path = r"json_config/test_config/config_path_TEST_NABLER.json"
    elif test_mode or test_mode == 't':
        print "TEST MODE"
        config_file_path = r"json_config/test_config/config_path_TEST.json"
    elif test_mode == 'p':
        print "PROD MODE"
        config_file_path = r"json_config/config_path.json"
    else:
        print "PROD MODE"
        config_file_path = r"json_config/config_path.json"

    configuration_manager = ConfigManager(path_to_master_config=config_file_path)
    if configuration_manager.get_load_status():
        controller_infrastructure = Infrastructure()
        if controller_infrastructure.is_ready():
            controller_infrastructure.start_setup()
        else:
            sys.exit("Issue with infrastructure")
    else:
        print "Could not load: {}".format(','.join(map(str, configuration_manager.get_list_of_failed_configs())))
        sys.exit("Issue with configuration settings")


if __name__ == '__main__':
    arg = False
    try:
        if sys.argv[1]:
            arg = sys.argv[1]
            print arg
    except IndexError:
        print "no arg"
    finally:
        main(test_mode=arg)

