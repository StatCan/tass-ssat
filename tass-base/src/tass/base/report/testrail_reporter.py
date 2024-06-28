import getpass
from tass.report.testrail.reporter import TestRailReporter
from tass.report.testrail.testrail import TestRail

from ..log.logging import getLogger


log = getLogger(__name__)


class TestRailTassReporter(TestRailReporter):

    def __init__(self, connection, config):
        super().__init__(connection, config)
        self._case_list = set()
        
    def _connect(self, connection):
        if "user" in connection and connection["user"] != "~":
            uname = connection["user"]
        elif "user" in connection and connection["user"] == "~":
            uname = getpass.getuser()
        else:
            uname = input("Enter your testrail username.")

        if "host" in connection and connection["host"] != "~":
            host = connection["host"]
            user = f"{host}\{uname}"
        elif "host" in connection and connection["host"] == "~":
            user = uname
        else:
            host = input("Enter the host name.")
            user = f"{host}\{uname}"

        if "password" in connection:
            pword = connection["password"]
        else:
            pword = getpass.getpass(prompt=f"Enter password for {user}:")
        
        connection["user"] = user
        connection["password"] = pword
        super()._connect(connection)
        
    def start_report(self, run, *args, **kwargs):
        tr_run = {
            "name": run.title,
            "suite_id": None, # TODO: implement for multi suite mode
            "description": str(run),
            "include_all": True, # TODO: implement for partial suites
            "case_ids": None,
            "refs": None
            }
        
        tr_project_id = run.var("testrail")['project_id']
        
        response = super().start_report(tr_project_id, tr_run)
        run.var('testrail')['id'] = response['id']
        
    def report(self, run, *args, **kwargs):
        # TODO: implement option to report as you go
        results = []
        for case in run.completed_cases:
            id = self._get_case_id(case.uuid, run.var('testrail')['project_id'])
            status = self._get_status_id(case.status)
            if not id:
                log.warning("Unable to report on case: %s", uuid)
                continue
            elif not status:
                log.warning("Case was not started. Skipping report for: %s", uuid)
                continue
            steps = case.steps
            tr_steps = [{
                "status_id": self._get_status_id(s.get('status', 'not started')),
                "content": s.get('title', "step not defined")
                } for s in steps]
            result = {
                "case_id": id,
                "status_id": status,
                "custom_step_results" : tr_steps
            }
            results.append(result)
            
        r = {
            "run_id": run.var('testrail')['id'],
            "results": {"results": results}
        }
        
        super().report(r)
            
    def _get_status_id(self, status):
        match status:
                case 'not started':
                    return None
                case 'incomplete':
                    return 2
                case 'failed':
                    return 5
                case 'passed':
                    return 1

    def _get_case_id(self, uuid, project_id):
        
        id = None
        
        def _case_id(case):
            return case[0] == project_id and case[1] == uuid
        case_ = filter(_case_id, self._case_list)
        try:
            id = next(case_)[2]
        except StopIteration:
            log.info("Case with uuid: %s not found in memory. Loading cases from Testrail", uuid)
            cases = self._testrail.cases().get_cases(project_id)
            
            self._case_list.update(
                    [(project_id, c['custom_tasscid'], c['id']) for c in cases]
                )
            
            case_ = filter(_case_id, self._case_list)
            
                    
            try:
                id = next(case_)[2]
            except StopIteration:
                log.warning("No case with TASS uuid: %s was found", uuid)
            
        return id
            