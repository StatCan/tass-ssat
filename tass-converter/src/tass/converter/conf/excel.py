import openpyxl


k_V_PARAMS = ["page", "stored_filter", "locator", "offset", "delta", "target"]
EOF = '//end//'

def convert(path):
    """
    Helper tool to convert xlsx config file to a in-memory json equivalent.
    """
    wb = openpyxl.load_workbook(path, data_only=True)  # Open excel file.
    wb.name = path.resolve().name

    s_runs = []  # Holds all test_run worksheet names.
    s_cases = []  # Holds all test_case worksheet names.
    s_reporters = []  # Holds all reporter worksheet names.
    s_browsers = []  # Holds all the browser worksheet names.
    s_mobiles = [] # Holds all the mobile worksheet names.
    s_hooks = [] # Holds all hook definitions worksheet names.

    # Get all worksheet names per type.
    for sheet in wb.sheetnames:

        tab_type = wb[sheet]['A1'].value
        if tab_type == 'tr_uuid:':
            s_runs.append(sheet)
        elif tab_type == 'tc_uuid:':
            s_cases.append(sheet)
        elif tab_type == 'r_uuid:':
            s_reporters.append(sheet)
        elif tab_type == 'br_uuid:':
            s_browsers.append(sheet)
        elif tab_type == 'mb_uuid:':
            s_mobiles.append(sheet)
        elif tab_type == "hooks":
            s_hooks.append(sheet)
        else:
            print('Not a tass Excel template.')

    # Extract configurations from sheets using sheet names
    # Extract cases and steps from sheets
    cases, steps = convert_cases(s_cases, wb)
    # Extract browser configs from sheets
    browsers = convert_browsers(s_browsers, wb)
    # Extract mobile configs from sheets
    mobiles = convert_mobiles(s_mobiles, wb)
    # Extract hook definitions from sheets
    hooks = convert_hooks(s_hooks, wb)
    # Extract all jobs to executed as a list.
    runs = convert_runs(s_runs, cases, steps, browsers, mobiles, hooks, wb)
    # TODO: define and print reporters.
    # reporters = convert_reporters(s_reporters, wb)

    return runs


def convert_hooks(hooks, wb):
    if not hooks:
        return {}
    _hooks = {}
    header_row = 2
    for sheet in hooks:
        for row in wb[sheet].iter_rows(min_row=3, max_col=6):
            _uuid = row[0].value
            _name = row[1].value
            _ns = row[2].value
            _when = row[3].value
            _critical = row[4].value
            _order = row[5].value
            _args = {}
            for col in wb[sheet].iter_cols(min_row=row[0].row,
                                            max_row=row[0].row,
                                            min_col=7):
                key = wb[sheet][header_row][col[0].column-1].value
                if key == EOF:
                    break
                val = col[0].value
                if val:
                    _args[key] = val

            hook_out = {
                "uuid": _uuid,
                "name": _name,
                "namespace": _ns,
                "when": _when,
            }

            if _critical is not None:
                hook_out["critical"] = bool(_critical)
            if _order is not None:
                hook_out["order"] = int(_order)

            _hooks[_uuid] = hook_out

    return _hooks


def convert_cases(cases, wb):
    if not cases:
        return {}, {}
    _cases = {}  # Dict of all test cases. Ensures unique case ids.
    _steps = {}  # Dict of all test steps. Ensures unique step ids.

    for c in cases:
        tc = {}  # Test case dict, to be printed in JSON
        tc["uuid"] = wb[c]['B1'].value

        if tc['uuid'] in _cases:
            print('UUID already exists. Skipping this case.')
            continue
        tc["title"] = wb[c]['D1'].value
        tc["steps"] = []
        hooks = wb[c]["F1"].value
        if hooks:
            tc["hooks"] = str(hooks).split(",")
        else:
            tc["hooks"] = []

        for row in wb[c].iter_rows(min_row=3, max_col=6):
            if (row[0] is None or row[0] == ''):
                continue
            steps = {}
            parameters = {}
            row_num = row[0].row
            valid = all(
                [row[0].value,
                isinstance(row[0].value, str),
                row[1].value,
                isinstance(row[1].value, str),
                row[2].value,
                isinstance(row[2].value, str),
                "," in str(row[2].value)]
            )

            if not valid:
                print(f"Case: {tc['uuid']} Row: {row_num} Step is missing mandatory fields UUID, TITLE, or ACTION.")
                continue
            steps["uuid"] = row[0].value
            steps["title"] = row[1].value
            steps["action"] = row[2].value.split(',', maxsplit=1)

            # The locator value is split on the comma
            for col in wb[c].iter_cols(min_row=row_num,
                                       max_row=row_num,
                                       min_col=4):

                header = wb[c].cell(2, col[0].column).value

                if (header == EOF):  # e.o.f indicator for TASS
                    break

                header = header.lower()

                if (col[0].value is not None):

                    # locator parameter.
                    # key,value pair or single string.
                    # ',' is reserved character.
                    if header in k_V_PARAMS:
                        param = str(col[0].value).split(',', maxsplit=1)
                    if header in k_V_PARAMS:
                        param = str(col[0].value).split(',', maxsplit=1)

                        if header == 'locator' or header == 'target':
                            if (len(param) == 2):
                                parameters[header] = {
                                    'by': param[0],
                                    'value': param[1]
                                }
                            else:
                                parameters[header] = param[0]
                        elif header == 'offset':
                            parameters['xoffset'] = int(param[0])
                            parameters['yoffset'] = int(param[1])
                        elif header == 'delta':
                            parameters['deltax'] = int(param[0])
                            parameters['deltay'] = int(param[1])
                        if header == 'locator' or header == 'target':
                            if (len(param) == 2):
                                parameters[header] = {
                                    'by': param[0],
                                    'value': param[1]
                                }
                            else:
                                parameters[header] = param[0]
                        elif header == 'offset':
                            parameters['xoffset'] = int(param[0])
                            parameters['yoffset'] = int(param[1])
                        elif header == 'delta':
                            parameters['deltax'] = int(param[0])
                            parameters['deltay'] = int(param[1])
                        else:
                            parameters[header] = param

                    # action parameter. read as "module,action"
                    elif ('action' in header):
                        parameters['action'] = (col[0]
                                                .value
                                                .split(',', maxsplit=1))

                    elif (header == 'locator_args'):
                        # locator_args parameter.
                        # "," separated list of arguments for locator.
                        # arguments are filled in order
                        # of definition at run time.
                        parameters[header] = (str(col[0].value)
                                              .split(','))

                    else:
                        parameters[header] = col[0].value

            # Adds the uuid to the corresponding test case list of steps.
            tc["steps"].append(steps["uuid"])
            # This block checks to see if a step with the same uuid but
            # different values already exists. If it does, the uuid is not
            # added to the list of steps and a message is printed.
            # The title is not checked as it has no bearing on function.
            # TODO: add better way of reporting (logger? exception?)
            if row[0].value in _steps:
                if ((_steps[row[0].value]["uuid"] == steps["uuid"])
                    and (_steps[row[0].value]["action"] ==
                         steps["action"])
                    and (_steps[row[0].value]['parameters'] ==
                         parameters)):
                    pass   # Do nothing
                else:
                    print("Different steps with uuid: " + row[0].value)
            else:
                steps['parameters'] = parameters
                _steps[row[0].value] = steps

        _cases[tc['uuid']] = tc
    return _cases, _steps


def convert_browsers(browsers, wb):
    if not browsers:
        return {}
    conf = {}
    for browser in browsers:
        b = {}  # Browser definition dict
        s = wb[browser]  # Browser definition worksheet

        browser_name = s['D1'].value
        uuid = s['B1'].value

        b_args = set()  # Browser arguments (flags)
        b_pref = {}  # Browser preferences (key/value)
        d_config = {}  # Driver configurations

        # Get Driver and browser arguments/config from sheet
        for row in s.iter_rows(min_row=3, min_col=2, max_col=6):
            if row[0].value:
                k, v = row[0].value.split(',', maxsplit=1)
                d_config[k] = v
            if row[2].value:
                b_args.add(row[2].value)
            if row[4].value:
                k, v = row[4].value.split(',', maxsplit=1)
                b_pref[k] = v

        config = {
            'driver': d_config,
            'browser': {
                'arguments': sorted(list(b_args)),
                'preferences': b_pref
                }
            }

        b['browser_name'] = browser_name
        b['uuid'] = uuid
        b['configs'] = config

        hooks = s["F1"].value
        if hooks:
            b["hooks"] = str(hooks).split(",")
        else:
            b["hooks"] = []

        conf[uuid] = b
    return conf


def convert_mobiles(mobiles, wb):
    if not mobiles:
        return {}
    conf = {}
    for mobile in mobiles:
        m = {}
        s = wb[mobile]  # Mobile definition worksheet

        platform_name = s['D1'].value
        uuid = s['B1'].value

        b_args = set()  # Browser arguments (flags)
        b_pref = {}  # Browser preferences (key/value)
        d_config = {}  # Driver configurations
        a_server = {} # Appium server configurations
        a_driver = {} # Appium driver configurations
        sb_driver = set() # Setup scripts for driver
        sa_driver = set() # Tear down scripts for driver

        for row in s.iter_rows(min_row=3, min_col=2, max_col=14):
            if row[0].value:
                k, v = row[0].value.split(',', maxsplit=1)
                d_config[k] = v
            if row[2].value:
                b_args.add(row[2].value)
            if row[4].value:
                k, v = row[4].value.split(',', maxsplit=1)
                b_pref[k] = v
            if row[6].value:
                _ = row[6].value.split(',', maxsplit=1)
                if len(_) == 2:
                    k, v = _
                else:
                    k = _[0]
                    v = True
                a_server[k] = v
            if row[8].value:
                _ = row[8].value.split(',', maxsplit=1)
                if len(_) == 2:
                    k, v = _
                else:
                    k = _[0]
                    v = True
                a_driver[k] = v
            if row[10].value:
                sb_driver.add(row[10].value)
            if row[12].value:
                sa_driver.add(row[12].value)

        config = {
            'driver': d_config,
            'browser': {
                'arguments': sorted(list(b_args)),
                'preferences': b_pref,
                },
            "scripts": {
                    "driver:setup": list(sb_driver),
                    "driver:teardown": list(sa_driver)
                },
            'appium:server': a_server,
            'appium:driver': a_driver
        }

        m["platform_name"] = platform_name
        m["uuid"] = uuid
        m["configs"] = config

        hooks = s["F1"].value
        if hooks:
            m["hooks"] = str(hooks).split(",")
        else:
            m["hooks"] = []

        conf[uuid] = m
    return conf

def  convert_runs(runs, cases, steps, browsers, mobiles, hooks, wb):
    if not runs:
        return []
    execs = []  # Holds all ready-to-run test runs as dict

    for run in runs:
        tr = {}  # Test run to be built
        ts = wb[run]  # Excel sheet containing test run configs.
        # ///// This information is converted to a Job.
        uuid = ts['B1'].value
        build = ts['B2'].value or "000"
        title = ts['D1'].value or "TASS JOB"
        parent = wb.name

        job = {
            "uuid": uuid,
            "build": build,
            "title": title,
            "parent": parent,
            "hooks": []
            }

        tr["Job"] = job
        tr["schema-version"] = "1.2.0"
        # \\\\\

        # ///// Create custom Logger as applicable
        if ts["D2"].value:
            logger_path = ts["D2"].value
            tr["Logger"] = {"path": logger_path}
        # \\\\\

        caseset = set()
        driverset = set()
        stepset = set()
        hookset = set()
        if ts["F1"].value:
            jobhooks = list(dict.fromkeys(str(ts["F1"].value).split(",")))
            job["hooks"] = jobhooks
            hookset.update(jobhooks)
        
        for row in wb[run].iter_rows(min_row=3, min_col=2, max_col=8):
            # Add cases ids
            if row[2].value:
                caseset.add(row[2].value)
            # Add browsers ids
            if row[6].value:
                driverset.add(row[6].value)

        # TODO: Optimize this? Move down to perform inside existing case loop
        for case in caseset:
            # Add step ids
            c = cases[case]
            for step in c['steps']:
                stepset.add(step)

        # Extract cases for this job
        tr["Cases"] = sorted([cases[c] for c in caseset],
                             key=lambda x: x['uuid'])
        # Extract steps for this job
        tr["Steps"] = sorted([steps[s] for s in stepset],
                             key=lambda x: x['uuid'])
        # Extract browsers and mobiles for this job
        tr["Browsers"] = sorted([browsers[b] for b in driverset if b in browsers],
                                key=lambda x: x['uuid'])

        tr["Mobiles"] = sorted([mobiles[b] for b in driverset if b in mobiles],
                                key=lambda x: x['uuid'])

        tests = []
        for driver in driverset:
            # extract hooks by browser and device
            if driver in browsers:
                driverhooks = list(dict.fromkeys(browsers[driver].get("hooks", [])))
            else:
                driverhooks = list(dict.fromkeys(mobiles[driver].get("hooks", [])))
            
        # "Explode" test cases + configurations
            for c in caseset:
                casehooks = list(dict.fromkeys(cases[c].get("hooks", [])))
                uuid = "--".join([job['uuid'], c, driver])  # Hybrid uuid
                test = {
                    "uuid": uuid,
                    "case": c,
                    "configurations": [
                        {
                            "type": "browser" if driver in browsers else "mobile",
                            "uuid": driver
                        }
                    ],
                }

                hookset.update(casehooks)
                tests.append(test)

            hookset.update(driverhooks)
            
        tr["Hooks"] = sorted([hooks[h] for h in hookset],
                                key=lambda x: x['uuid'])
        tr['Tests'] = sorted(tests, key=lambda x: x['uuid'])

        # other attributes:
        for col in wb[run].iter_cols(min_row=3, max_row=3, min_col=10):
            if not col or col[0].value is None:
                continue
            header = col[0].value
            col_num = col[0].column
            attr = {}
            for row in wb[run].iter_rows(min_row=4,
                                         min_col=col_num,
                                         max_col=col_num):
                if not row or row[0].value is None:
                    continue
                k, v = row[0].value.split(",", maxsplit=1)
                attr[k] = v
            tr[header] = attr

        execs.append(tr)

    return execs


def convert_reporters(reporters, wb):
    # TODO: define reporters
    if not reporters:
        return {}
    pass
