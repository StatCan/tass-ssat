import argparse
import json
import tass.log.logging
from pathlib import Path
from tass.core.tass_files import TassRun


log = logging.getLogger(__name__)

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


def main(args):
    """
    Starting point for execution of tests.
    """
    log.info('Using: {}', args.file)
    with open(args.file) as file:
        # open the test file and load into memory as TassRun
        log.debug('Succesfully opened {}', file)
        # TODO: TassRun or Tass Suite can be executed
        j_runs = read_file(file)
    runs = []
    for run in j_runs:
        test = TassRun(args.file, browser=args.browser, **run)

        for case in test.collect():
            # collect test cases from file
            print(case)
            case.execute_tass()
            print('/ / / / / / / / / / / / / / / / / / / /')

        runs.append(test)

    # Write results to file
    Path('results').mkdir(exist_ok=True)

    for test in runs:
        file_name = test.uuid + '---' + test.start_time + '.json'
        result_path = Path().resolve() / "results" / file_name
        with open(result_path, 'w+', encoding='utf-8') as f:
            json.dump(test, f, indent=4, cls=TassEncoder)


def read_file(file):
    _test = json.load(file)
    log.info("Loading ")
    
    steps = _test.get('Steps', [])
    log.debug("Loaded steps: {}", steps)

    test_cases = _test.get('Test_cases', [])
    log.debug("Loaded cases: {}", test_cases)

    # test_suites = _test.get('Test_suites', [])
    test_runs = _test.get('Test_runs', [])
    log.debug("Loaded runs: {}", test_runs)

    def read_cases(run):
        _cases = []
        for case in run.get('test_cases', []):
            _steps = []
            _case = next(filter(lambda _c: _c['uuid'] == case, test_cases))
            for step in _case.get('steps', []):
                print(step)
                _steps.append(next(
                    filter(lambda _c: _c['uuid'] == step, steps)))
            _case['steps'] = _steps
            _cases.append(_case)
        run['test_cases'] = _cases

    for run in test_runs:
        # _suites = []
        read_cases(run)

    return test_runs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', "-f",
                        action='store', required=True)
    parser.add_argument('--browser', "-b",
                        type=str.lower,
                        action='store', required=True)

    main(parser.parse_args())
