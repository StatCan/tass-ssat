import openpyxl

def convert(path):
    """
    Helper tool to convert xlsx config file to a in-memory json equivalent.
    """
    conf_file = {}
    conf_file["Test_runs"] = []
    conf_file["Test_suites"] = []
    conf_file["Test_cases"] = []
    conf_file["Steps"] = []
    wb = openpyxl.load_workbook(path) # Open conf file.

    test_run = []
    test_suite = []
    test_case = []
    test_steps = []

    for sheet in wb.sheetnames:
        
        test_type = wb[sheet]['A1'].value

        if test_type == 'tr_uuid:':
            test_run.append(sheet)
        elif test_type == 'ts_uuid:':
            test_suite.append(sheet)
        elif test_type == 'tc_uuid:':
            test_case.append(sheet)
        else:
            print('Not a tass Excel template.')
    
    print(test_run)
    print(test_suite)
    print(test_case)

    if test_run:
        conf_file = convert_test_run(test_run, conf_file, wb)
    if test_suite:
        conf_file = convert_test_suite(test_suite, conf_file, wb)
    if test_case:
        conf_file = convert_test_case(test_case, conf_file, wb)
    print("Printing conf file")
    print(conf_file)

    return conf_file

def convert_test_case(test_case, conf, wb):
    conf["Test_cases"] = []
    for case in test_case:
        tc = {}
        tc["tc_uuid"] = wb[case]['B1'].value
        tc["title"] = wb[case]['D1'].value
        tc["steps"] = []
        for row in wb[case].iter_rows(min_row=3, max_col=4):
            steps = {}
            tc["steps"].append(row[0].value)
            steps["uuid"] = row[0].value
            steps["title"] = row[1].value
            steps["action"] = row[2].value
            steps["parameter"] = row[3].value
            conf["Steps"].append(steps)

        conf["Test_cases"].append(tc)
    return conf

def convert_test_suite(test_suite, conf, wb):
    conf["Test_suites"] = []
    for suite in test_suite:
        ts = {}
        ts["uuid"] = wb[suite]['B1'].value
        ts["test_cases"] = []
        ts["keywords"] = []
        for row in wb[suite].iter_rows(min_row=2, min_col=2, max_col=2):
            if row[0].value is not None:
                ts["test_cases"].append(row[0].value)
        for row in wb[suite].iter_rows(min_row=1, min_col=4, max_col=4):
            if row[0].value is not None:
                ts["keywords"].append(row[0].value)
        conf["Test_suites"].append(ts)

    return conf

def convert_test_run(test_run, conf, wb):
    conf["Test_runs"] = []
    for run in test_run:
        tr = {}
        tr["uuid"] = wb[run]['B1'].value
        tr["build"] = wb[run]['B2'].value
        tr["start_time"] = wb[run]['D1'].value
        tr["end_time"] = wb[run]['D2'].value
        tr["test_cases"] = []
        tr["test_suites"] = []
        for row in wb[run].iter_rows(min_row=3, min_col=2, max_col=2):
            if row[0].value is not None:
                tr["test_suites"].append(row[0].value)
        for row in wb[run].iter_rows(min_row=3, min_col=4, max_col=4):
            if row[0].value is not None:
                tr["test_cases"].append(row[0].value)
        conf["Test_runs"].append(tr)

    return conf
