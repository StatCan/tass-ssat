import json
from pathlib import Path
from .schema.parse import parse
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


def execute(file_path, no_validate):
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")

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
