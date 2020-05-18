import sys

from infrastructure import Infrastructure


def main(test_mode=False):
    if test_mode:
        config_file_path = r"config/json_config/test_config/config_path.json"
    else:
        config_file_path = r'config/json_config/config_path.json'

    controller_infrastructure = Infrastructure(config_file_path=config_file_path)

    if controller_infrastructure.is_ready():
        controller_infrastructure.start_setup()
    else:
        sys.exit("Issue with infrastructure")


if __name__ == '__main__':
    main(test_mode=True)
