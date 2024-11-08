import argparse
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


def main(args):
    """
    Starting point for execution of tests.
    """
    log.info("\n\n <<<<<< TASS Starting >>>>>> \n\n")

    path = Path(args.file).resolve()

    test = parse(path, args.no_validate)

    log.info("<<<<< Starting Run: %s >>>>>", test.uuid)
    for case in test.collect():
        log.info("")
        log.info("< < < Starting Case: %s > > >", case.uuid)
        log.info("")

        case.execute_tass()

        log.info("")
        log.info("> > > Finished Case: %s < < <", case.uuid)
        log.info("")

    Path('results').mkdir(exist_ok=True)

    file_name = test.uuid + '---' + test.start_time + '.json'
    result_path = Path().resolve() / "results" / file_name
    try:
        f = open(result_path, 'w+', encoding='utf-8')
    except IOError as e:
        log.error("An IOError occured: %s" % e)
        return
    with f:
        json.dump(test, f, indent=4, cls=TassEncoder)


if __name__ == '__main__':

    # automated browser testing tool parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', "-f",
                        action='store', required=True)

    parser.add_argument('--no-validate', action='store_false',
                        default=True)

    args = parser.parse_args()
    log.debug("Launch arguments:", vars(args))
    main(args)
