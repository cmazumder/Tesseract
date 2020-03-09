import sys

from setup import controller_infrastructure_ready, start_controller_setup


def main(test_mode=0):
    if controller_infrastructure_ready():
        start_controller_setup(test_mode)
    else:
        sys.exit("Issue with infrastructure")


if __name__ == '__main__':
    main(0)
