import getpass
import logging
from .reporter import TestrailReporter


log = logging.getLogger("tass.report")


class TassTestrailReporter(TestrailReporter):

    def __init__(self, connection, config,
                 case_map, runs, plans,
                 project_id,
                 *args, **kwargs):
        super().__init__(connection, config, *args, **kwargs)
        self._map = case_map # dictionary -> {testrail id: tass uuid}
        self._runs = runs
        self._plans = plans
        self._project_id = project_id
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
            user = f"{host}\\{uname}"
        elif "host" in connection and connection["host"] == "~":
            user = uname
        else:
            host = input("Enter the host name.")
            user = f"{host}\\{uname}"

        if "password" in connection:
            pword = connection["password"]
        else:
            pword = getpass.getpass(prompt=f"Enter password for {user}:")

        connection["user"] = user
        connection["password"] = pword
        return super()._connect(connection)

    def start_report(self, result, *args, **kwargs):
        if self._plans:
            # TODO: create plans with api
            for plan in self._plans:
                _plan = {
                    "name": _plan["name"],
                    "description": _plan["description"],
                    "project_id": self._project_id
                }
        else:
            # TODO: create runs with api
            pass

    def _create_plan(self, id, plan):
        # TODO: create plan json to send to API
        pass

    def _create_run(self, id, run):
        # TODO: create run json to send to API
        pass

    def report(self, run, *args, **kwargs):
        # TODO: prepare runs for api calls
        pass

    def end_report(self, run, *args, **kwargs):
        # TODO: close out runs as described in configs.
        pass

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
