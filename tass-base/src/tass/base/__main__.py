import argparse
import json
from pathlib import Path
from .core.tass_files import TassRun
from .log.logging import getLogger
from tass.report.registrar import ReporterRegistrar


log = getLogger(__name__)


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


def _make_report(registrar, func_name, *args, **kwargs):
    if registrar:
        for reporter in registrar.iter_reporters():
            getattr(reporter, func_name)(*args, **kwargs)


def main(args):
    """
    Starting point for execution of tests.
    """
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")
    log.info("Preparing run using: %s", args.file)

    with open(args.file) as file:
        # open the test file and load into memory as TassRun
        # TODO: TassRun or Tass Suite can be executed
        j_runs, registrar = _read_file(file)
    runs = []

    for run in j_runs:
        test = TassRun(args.file, browser=args.browser, **run)
        log.info("Ready to start test: %s-(%s)", test.title, test.uuid)

        _make_report(registrar, "start_report", test)
        for case in test.collect():
            # collect test cases from file
            log.info(">>>>> Starting Test Case: %s - (%s) <<<<<",
                     case.title, case.uuid)
            log.debug("Test Case details: %r", case)
            case.execute_tass()
            log.info("<<<<< Finished Test Case: %s - (%s) >>>>>",
                     case.title, case.uuid)

        runs.append(test)
        _make_report(registrar, "report", test)
        _make_report(registrar, 'end_report', test)
    # Write results to file
    Path('results').mkdir(exist_ok=True)

    for test in runs:
        file_name = test.uuid + '---' + test.start_time + '.json'
        result_path = Path().resolve() / "results" / file_name
        with open(result_path, 'w+', encoding='utf-8') as f:
            json.dump(test, f, indent=4, cls=TassEncoder)


def _read_file(file):

    _test = json.load(file)
    log.info("Reading job file...")
    log.debug("Loaded file: %s", _test)

    steps = _test.get('Steps', [])
    test_cases = _test.get('Test_cases', [])
    reporters = _test.get('Reporters', [])

    # test_suites = _test.get('Test_suites', [])
    test_runs = _test.get('Test_runs', [])

    def read_cases(run):
        _cases = []
        log.info("Reading test cases...")
        for case in run.get('test_cases', []):
            log.info("Looking for Test Case uuid: %s", case)

            _steps = []
            _case = next(filter(lambda _c: _c['uuid'] == case, test_cases))

            log.info("Found test case: %s", _case['title'])
            log.debug("Test case details: %r", _case)
            log.info("Reading steps for case...")
            for step in _case.get('steps', []):
                log.info("Looking for Step uuid: %s", step)
                _step = next(filter(lambda _c: _c['uuid'] == step, steps))

                log.info("Found step: %s", _step['title'])
                log.debug("Step details: %r", _step)
                _steps.append(_step)

            _case['steps'] = _steps

            managers = set([_m['action'][0].lower() for _m in _steps])
            log.info("Using modules: %r", managers)

            _case['managers'] = managers
            log.info("Test case, '%s' read complete", _case['title'])
            log.debug("Prepared Test Case: %r", _case)

            _cases.append(_case)
        run['test_cases'] = _cases

    log.info("Collecting test runs...")
    for run in test_runs:
        # _suites = []
        log.info("Reading run: %s", run['uuid'])
        log.debug("Run details: %r", run)
        read_cases(run)

    registrar = None
    if reporters:
        registrar = ReporterRegistrar()
        for reporter in reporters:
            registrar.register_reporter(**reporter)

    return test_runs, registrar


if __name__ == '__main__':

    # lists of choices for parser options
    supported_browsers = ['chrome', 'firefox', 'edge']

    parser = argparse.ArgumentParser()

    # automated browser testing tool parser

    parser.add_argument('--file', "-f",
                        action='store', required=True)
    parser.add_argument('--browser', "-b",
                        type=str.lower, required=True,
                        action='store', choices=supported_browsers)

    args = parser.parse_args()
    log.debug("Launch arguments:", vars(args))
    main(args)
