import sys

from ConfigManager.ConfigManager import ConfigManager
from InfrastructureSetup import InfrastructureSetup


def main(test_mode=False):
    if test_mode == 'testV':
        print "TEST MODE VERTEX"
        config_file_path = r"configuration/test_config/config_path_TEST_VERTEX.json"
    elif test_mode == 'testN':
        print "TEST MODE NABLER"
        config_file_path = r"configuration/test_config/config_path_TEST_NABLER.json"
    elif test_mode == 'test':
        print "TEST MODE"
        config_file_path = r"configuration/config_path.json"
    elif test_mode or test_mode == 't':
        print "Dummy test MODE"
        config_file_path = r"configuration/test_config/config_path_TEST.json"
    elif test_mode == 'prod':
        print "PROD MODE"
        config_file_path = r"configuration/config_path.json"
    else:
        print "PROD MODE"
        config_file_path = r"configuration/config_path.json"

    print "Using {}".format(config_file_path)
    configuration_manager = ConfigManager(path_to_master_config=config_file_path)
    if configuration_manager.get_load_status():
        controller_infrastructure = InfrastructureSetup()
        if controller_infrastructure.is_ready():
            if test_mode == 'test':
                sys.exit("Infrastructure is ready")
            else:
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
            print "Mode: {}" .format(arg)
    except IndexError:
        print "No argument"
    finally:
        main(test_mode=arg)
