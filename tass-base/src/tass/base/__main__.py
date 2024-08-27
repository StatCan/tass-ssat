import argparse
import json
from pathlib import Path
from tass.report.registrar import ReporterRegistrar
from .actions.action_manager import get_manager
from .core.tass_files import TassRun
from .log.logging import getLogger

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

def main(args):
    """
    Starting point for execution of tests.
    """
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")
    log.info("Preparing run using: %s", args.file)

    path = Path(args.file).resolve()
    with open(path) as f:
        job = json.load(f)

    runs = parse_runs(path, job)

    for test in runs:
        for case in test.collect():
            case.execute_tass()

    Path('results').mkdir(exist_ok=True)
    for test in runs:
        file_name = test.uuid + '---' + test.start_time + '.json'
        result_path = Path().resolve() / "results" / file_name
        with open(result_path, 'w+', encoding='utf-8') as f:
            json.dump(test, f, indent=4, cls=TassEncoder)

    # TODO: Parse Suites
    # TODO: add logging messages.

def parse_runs(path, job):
    all_runs = job.get('Test_runs')
    ready_runs = []

    for run in all_runs:
        run['test_cases'], managers = parse_cases(job, run)
        for browser in parse_browsers(job):
            _managers = {}
            for _manager in managers:
                if _manager not in _managers:
                    _managers.update(get_manager(_manager, config=browser))
            
            _run = TassRun(path, action_managers=_managers, **run)

            ready_runs.append(_run)

    return ready_runs

def parse_suites(job):
    pass


def parse_cases(job, run):
    
    cases = []
    test_cases = job.get('Test_cases', [])
    all_steps = job.get('Steps', [])
    for case_id in run.get('test_cases', []):
        steps = []
        case = next(filter(lambda _c: _c['uuid'] == case_id, test_cases))

        for step in case.get('steps', []):
            _ = next(filter(lambda _c: _c['uuid'] == step, all_steps))

            steps.append(_)
        
        case['steps'] = steps
        
        managers = set([_m['action'][0].lower() for _m in steps])

        cases.append(case)
    
    return cases, managers


def parse_reporters(job): 
    registrar = ReporterRegistrar()
    reporters = job['Reporters']

    for reporter in reporters:
        registrar.register_reporter(**reporter)
    
    return registrar


def parse_browsers(job):
    browsers = job['Browsers']
    for browser in browsers:
        yield browser

if __name__ == '__main__':

    # automated browser testing tool parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', "-f",
                        action='store', required=True)

    args = parser.parse_args()
    log.debug("Launch arguments:", vars(args))
    main(args)
