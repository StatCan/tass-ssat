import openpyxl

def convert(path):

    conf_file = {}
    wb = openpyxl.load_workbook(path)
    ws = wb.active

    header = []
    for cell in ws[1]:
        header.append(cell.value)

    conf_file['steps'] = []

    for row in ws.iter_rows(min_row=2):
        steps = {}
        index = 0
        while index < len(header):
            
            steps[header[index]] = row[index].value

            index += 1

        conf_file['steps'].append(steps)

    return conf_file

