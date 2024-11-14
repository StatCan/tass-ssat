import argparse
import json


def main(reporter, file):
    pass

if __name__ is "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--reporter", "-r", required=True)
    parser.add_argument("--file", "-f", required=True)

    # TODO: Add arguments for:
    # --no-validation -> Skip schema validation
    # --force-overwrite -> Do not prompt for file overwrite
    # --report-name -> Use given file name for report

    args = parser.parse_args()

    main(**vars(args))

