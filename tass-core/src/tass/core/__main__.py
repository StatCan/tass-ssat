import argparse
from .log import logging
from .execute import execute


def main(file_paths, no_validate, run_logging, test_logging, log_level):
    """
    Starting point for execution of tests.
    """
    execute(file_paths, no_validate, run_logging, test_logging, log_level)


if __name__ == '__main__':

    # automated browser testing tool parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', "-f", dest="file_paths",
                        required=True, nargs="+")

    parser.add_argument('--no-validate', action='store_true')
    
    # TODO: Add argument for no run logging
    parser.add_argument('--disable-run-logging', action="store_true",
                        dest="run_logging")
    # TODO: Add argument for no test logging
    parser.add_argument('--disable-test-logging', action="store_true",
                        dest="test_logging")
    # TODO: Add argument for log level?
    parser.add_argument('--log-level', '-ll', action="store",
                        choices=["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", dest="log_level",
                        type=str.upper)
    parser.add_argument('--verbose', '-v', action="store_const",
                        dest="log_level", const="DEBUG")

    args = parser.parse_args()
    main(**vars(args))
