import argparse
import json
from tass.core.tass_files import TassRun


def main(args):
    print(args.file)
    with open(args.file) as file:
        test = TassRun(args.file, **json.load(file))
        for case in test.collect():
            print(case)
            case.execute_tass()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                        action='store', required=True)

    main(parser.parse_args())
