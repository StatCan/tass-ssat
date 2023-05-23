import openpyxl

def convert(path):
    """
    Helper tool to convert xlsx config file to a in-memory json equivalent.
    """
    conf_file = {}
    wb = openpyxl.load_workbook(path) # Open conf file.
    ws = wb.active # First worksheet holds conf info.

    header = []
    for cell in ws[1]: # Assumes that first row is header info.
        header.append(cell.value)

    conf_file['steps'] = []

    # Loop goes through entire xlsx file from 2nd row onwards.
    # Each row is assumed to be a "step" in a config file.
    # Relevant information is extracted and assigned to a value
    # pulled from the header.
    for row in ws.iter_rows(min_row=2):
        steps = {}
        index = 0
        while index < len(header):
            
            steps[header[index]] = row[index].value

            index += 1

        conf_file['steps'].append(steps)

    return conf_file
