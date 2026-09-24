from ..log.logging import getLogger
from .validate import validate
import json


log = getLogger(__name__)


def parse(path, no_validate):
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
    return validate(job, no_validate).parse(path, job)
