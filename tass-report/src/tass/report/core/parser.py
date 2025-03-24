from tass.core.schemas.parser import Parser
from ..reporter_factory import get_reporter


reporters = {

}

class Testrail1Parser(Parser):
    def __init__(self):
        super.__init__(self)

    def parse(self, path, reporter):
        pass
