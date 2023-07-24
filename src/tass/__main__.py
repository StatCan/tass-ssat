import argparse
import json
from pathlib import Path
from tass.core.tass_files import TassRun


class TassEncoder(json.JSONEncoder):
    # Convert Python objects to JSON equivalent.
    # TODO: Update format to match test management tool
    def default(self, obj):
        """
        Default JSON encoder
        for custom TASS classes.
        Serializable TASS classes should
        implement the toJson function.
        """
        if (hasattr(obj, 'toJson')):
            return obj.toJson()
        else:
            raise TypeError(
                "Unserializable object {} of type {}".format(obj, type(obj))
                )


def load(file_path):
    with open(file_path) as file:
        test = json.load(file)
    match test['file-type']:
        case 'test-run':
            return TassRun.create(path=file_path,
                           **test['content'])


def main(args):
    """
    Starting point for execution of tests.
    """
    print(args.file)

    # open the test file and load into memory as TassRun
    # TODO: TassRun or Tass Suite can be executed
    test = load(args.file)
    for case in test.collect():
        # collect test cases from file
        print(case)
        case.execute_tass()
        print('/ / / / / / / / / / / / / / / / / / / /')

    # Write results to file
    Path('results').mkdir(exist_ok=True)

    file_name = test.uuid + '---' + test.start_time + '.json'
    result_path = Path().resolve() / "results" / file_name
    with open(result_path, 'w+', encoding='utf-8') as f:
        json.dump(test, f, indent=4, cls=TassEncoder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                        action='store', required=True)
    main(parser.parse_args())
