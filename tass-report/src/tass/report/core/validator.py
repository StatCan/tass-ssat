from . import parser
from ..testrail import schemas
from tass.core.schema.validator import Validator


class Testrail1Validator(Validator):
    def __init__(self):
        super.__init__(schemas.TESTRAIL_1_0_0)

    def parser(self):
        return parser.Testrail1Parser()