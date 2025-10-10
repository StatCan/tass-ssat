import argparse
from .log.logging import getLogger
from .execute import execute


log = getLogger(__name__)


def main(file_path, no_validate):
    """
    Starting point for execution of tests.
    """
    execute(file_path, no_validate)


if __name__ == '__main__':

    # automated browser testing tool parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', "-f", dest="file_path",
                        action='store', required=True)

    parser.add_argument('--no-validate', action='store_false',
                        default=True)

    args = parser.parse_args()
    log.debug("Launch arguments:", vars(args))
    main(**vars(args))
