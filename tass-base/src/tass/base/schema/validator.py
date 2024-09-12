from . import parser
from . import schemas
from jsonschema import Draft7Validator

class Validator():
    def __init__(self, schema):
        self.validator = Draft7Validator
        self.schema = schema

    def validate(self, job):
        self.validator.check_schema(self.schema)
        self.validator(self.schema).validate(job)
    
    def parser(self):
        raise NotImplementedError("No parser is implemented.")


class Tass1Validator(Validator):

    def __init__(self):        
        super().__init__(schemas.SCHEMA_1_0_0)
    
    def parser(self):
        return parser.Tass1Parser()