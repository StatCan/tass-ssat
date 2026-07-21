from tass.core.log.logging import getLogger
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from tass.core.parser import validator


log = getLogger(__name__)


DEFAULT = validator.Tass1_1Validator
DEFAULT_SCHEMA = "1.1.0"

def version_check(version, spec):
    return Version(version) in SpecifierSet(spec)


def validate(job, validate_on):
    log.info("Validating job file.")
    schema_version = job.get('schema-version', DEFAULT_SCHEMA)
    log.info("Using schema version: %s", schema_version)

    if version_check(schema_version, "<1.1"):
        log.info("Validating schema against schema version: 1.0.0")
        schema = validator.Tass1Validator()
    elif version_check(schema_version, "~=1.1"):
        log.info("Validating schema against schema version: 1.1.0")
        schema = validator.Tass1_1Validator()
    else:
        log.warning("Invalid schema version. Attempting default schema validation: {}", DEFAULT_SCHEMA)
        schema = DEFAULT()

    if validate_on:
        schema.validate(job)
    log.info("Validation successful.")
    return schema.parser()
