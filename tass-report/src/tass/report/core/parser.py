from tass.core.schema.parser import Parser
from ..reporter_factory import get_reporter


reporters = {

}

class Testrail1Parser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path, raw):
        return self._parse_raw_reporter(path, **raw)

    def _parse_raw_reporter(self, path, uuid,
                            connection, Cases,
                            Runs, project_id,
                            _type, Plans=[], package= None,
                            class_name=None,
                            config=None, **kwargs):
        reporter = {
            "path": path,
            "uuid": uuid,
            "connection": connection,
            "case_map": self._parse_case_map(Cases),
            "runs": Runs,
            "project_id": project_id,
            "_type": _type,
            "plans": Plans,
            "package": package,
            "class_name": class_name,
            "config": config
        }
        return get_reporter(**reporter, **kwargs)

    def _parse_case_map(self, cases):
        case_map = {}
        for c in cases:
            case_map[c["id"]] = c["tuuid"]
        return case_map