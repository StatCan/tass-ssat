from tass.base.log.logging import getLogger
from packaging.version import Version
from tass.base.schema import validator


log = getLogger(__name__)
DEFAULT = validator.Tass1Validator
DEFAULT_SCHEMA = "0.0.0"

def validate(job, validate_on):
    log.info("Validating job file.")
    schema_version = job.get('schema-version', DEFAULT_SCHEMA)
    log.info("Using schema version: %s", schema_version)

    version = Version(schema_version)

    if version >= Version('0.0.0'):
        log.info("Validating schema against schema version: 1.0.0")
        schema = validator.Tass1Validator()
    else:
        schema = DEFAULT()
    
    if validate_on:
        schema.validate(job)
    log.info("Validation successful.")
    return schema.parser()

