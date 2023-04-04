import argparse
import json
from pathlib import Path
from tass.drivers.browserdriver import toJson
from tass.core.tass_files import TassRun


class TassEncoder(json.JSONEncoder):
    # Convert Python objects to JSON equivalent.
    # TODO: Update format to match test management tool
    def default(self, obj):
        if (hasattr(obj, 'browser')):
            return toJson(obj)
        elif (hasattr(obj, 'toJson')):
            return obj.toJson()
        else:
            raise TypeError(
                "Unserializable object {} of type {}".format(obj, type(obj))
                )


def main(args):
    print(args.file)
    with open(args.file) as file:
        test = TassRun(args.file, **json.load(file))
        for case in test.collect():
            print(case)
            case.execute_tass()
            print('/ / / / / / / / / / / / / / / / / / / /')

    # Write results to file
    file_name = test.uuid + '---' + test.start_time + '.json'
    result_path = Path().resolve() / "results" / file_name
    with open(result_path, 'w+', encoding='utf-8') as f:
        json.dump(test, f, indent=4, cls=TassEncoder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                        action='store', required=True)

    main(parser.parse_args())
