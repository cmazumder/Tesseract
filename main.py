import sys

from config.config_manager import ConfigManager
from infrastructure import Infrastructure


def main(test_mode=False):
    if test_mode:
        config_file_path = r"json_config/test_config/config_path.json"
    else:
        config_file_path = r'json_config/config_path.json'

    configuration_manager = ConfigManager(path_to_master_config=config_file_path)
    if configuration_manager.get_load_status():
        controller_infrastructure = Infrastructure()
        if controller_infrastructure.is_ready():
            controller_infrastructure.start_setup()
        else:
            sys.exit("Issue with infrastructure")
    else:
        print "Could not load: {}".format(str(configuration_manager.get_list_of_failed_configs())[1:-1])
        sys.exit("Issue with configuration settings")


if __name__ == '__main__':
    main(test_mode=False)
