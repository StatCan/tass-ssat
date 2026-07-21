import json
from . import parser
from importlib import resources
from jsonschema import Draft7Validator
from ..log.logging import getLogger


class Validator():

    log = getLogger(__name__)

    def __init__(self, schema):
        self._validator = Draft7Validator
        self._schema = schema
        self._schema_obj = None

    @property
    def validator(self):
        return self._validator

    def schema_json(self):
        if self._schema_obj is None:
            schema_dir = resources.files("tass.core.schemas")
            _schema = schema_dir.joinpath(self._schema)
            try:
                f = open(_schema)
            except IOError as e:
                log.error("An IOError occured: %s" % e)
                return None

            with f:
                self._schema_obj = json.load(f)

        return self._schema_obj
    

    def validate(self, job):
        self.validator.check_schema(self.schema_json())
        self.validator(self.schema_json()).validate(job)

    def parser(self):
        raise NotImplementedError("No parser is implemented.")


class Tass1Validator(Validator):

    def __init__(self):
        super().__init__("tass_1.0.json")

    def validate(self, job):
        super().validate(job)
        # TODO: validate using uniqueness rules.

    def parser(self):
        return parser.Tass1Parser()


class Tass1_1Validator(Validator):

    def __init__(self):
        super().__init__("tass_1.1.json")

    def validate(self, job):
        super().validate(job)
        # TODO: validate using uniqueness rules.

    def parser(self):
        return parser.Tass1_1Parser()
