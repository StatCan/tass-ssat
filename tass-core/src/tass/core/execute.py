import json
from pathlib import Path
from .parser.parse import parse
from .log.logging import getLogger, init_base_logger


log = None


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
        if (isinstance(obj, object)):
            if (hasattr(obj, 'toJson')):
                return obj.toJson()
            elif isinstance(obj, Exception):
                return {"error": obj.__class__.__name__, "message": str(obj)}
        return super().default(obj)


def init_loggers(run_logging, test_logging, log_level):
    init_base_logger(run_logging=run_logging,
                     test_logging=test_logging,
                     log_level=log_level)
    return getLogger(__name__)

def execute(file_paths, no_validate, run_logging, test_logging, log_level):
    log = init_loggers(
                run_logging,
                test_logging,
                log_level)
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")
    for file_path in file_paths:
        path = Path(file_path).resolve()


        run = parse(path, no_validate)

        log.info("<<<<< Starting Run: %s >>>>>", run.uuid)
        for case in run.collect():
            log.info("")
            log.info("< < < Starting Case: %s > > >", case.uuid)
            log.info("")

            case.execute_tass()

            log.info("")
            log.info("> > > Finished Case: %s < < <", case.uuid)
            log.info("")

        Path('results').mkdir(exist_ok=True)

        file_name = run.uuid + '---' + run.start_time + '.json'
        result_path = Path().resolve() / "results" / file_name
        try:
            f = open(result_path, 'w+', encoding='utf-8')
        except IOError as e:
            log.error("An IOError occured: %s" % e)
            return
        with f:
            json.dump(run, f, indent=4, cls=TassEncoder)
