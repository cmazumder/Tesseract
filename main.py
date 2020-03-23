import sys

from infrastructure import controller_infrastructure_ready, start_controller_setup, config_file_select


def main(test_mode=False):
    config_file_select(test_mode)
    if controller_infrastructure_ready():
        start_controller_setup(test_mode)
    else:
        sys.exit("Issue with infrastructure")


if __name__ == '__main__':
    main(test_mode=False)
