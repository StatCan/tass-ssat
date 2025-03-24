from tass.core.log.logging import getLogger
from packaging.version import Version
from . import validator


log = getLogger(__name__)


DEFAULT = validator.Testrail1Validator
DEFAULT_SCHEMA = "0.0.0"


def validate(reporter, validate_on):
    log.info("Validating job file.")
    schema_version = reporter.get('schema-version', DEFAULT_SCHEMA)
    log.info("Using schema version: %s", schema_version)

    version = Version(schema_version)

    if version >= Version('0.0.0'):
        log.info("Validating schema against schema version: 1.0.0")
        schema = validator.Testrail1Validator()
    else:
        schema = DEFAULT()

    if validate_on:
        schema.validate(reporter)
    log.info("Validation successful.")
    return schema.parser()
