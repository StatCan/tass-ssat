from tass.core.log.logging import getLogger
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from tass.core.parser import validator


log = getLogger(__name__)


DEFAULT = validator.Tass1_1Validator
DEFAULT_SCHEMA = "1.1.0"

def version_check(version, spec):
    return Version(version) in SpecifierSet(spec)


def validate(job, no_validate):
    log.info("Checking job file schema version.")
    if "schema-version" not in job:
        log.warning("Schema version is not specified. Using default schema.")
    schema_version = job.get('schema-version', DEFAULT_SCHEMA)
    log.info("Using schema version: %s", schema_version)

    if version_check(schema_version, "<1.1"):
        schema = validator.Tass1Validator()
    elif version_check(schema_version, "~=1.1"):
        schema = validator.Tass1_1Validator()
    else:
        log.warning("Invalid schema version. Attempting to use default schema: {}", DEFAULT_SCHEMA)
        schema = DEFAULT()

    if not no_validate:
        schema.validate(job)
        log.info("Validation successful.")
    else:
        log.info("Skipping schema validation.")
    return schema.parser()
