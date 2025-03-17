from ..log.logging import getLogger
from .validate import validate
import json


log = getLogger(__name__)


def parse(path, validate_on=True):
    log.info("Preparing job using file @: %s", path)
    try:
        f = open(path)
        # open test file
    except IOError as e:
        log.error("An IOError occured: %s" % e)
        return
    with f:
        job = json.load(f)

    # Validation and parsing step
    return validate(job, validate_on).parse(path, job)
