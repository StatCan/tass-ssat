from .validate import validate
import json


def parse(path, validate_on=True):
    try:
        f = open(path)
        # open test file
    except IOError as e:
        return
    with f:
        job = json.load(f)

    # Validation and parsing step
    return validate(job, validate_on).parse(path, job)


def parse_result(path, validate_on=True):
    # TODO: validate results
    # TODO: return parsed results
    pass