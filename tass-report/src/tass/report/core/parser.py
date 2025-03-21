import jsonschema
import json
from pathlib import Path
from .reporter_factory import get_reporter


reporters = {

}

def parse_reporter(path, no_validate, **kwargs):
    if not no_validate:
        # TODO: skip validation
        pass

    try:
        with open(Path(path).resolve()) as f:
            raw = json.load(f)
    except Exception:
        # TODO handle Exception
        pass

    reporter =  get_reporter(**raw)
    return reporter

def read_file(path,  no_validate):
    # TODO: parse and validate reporter json file
    pass
