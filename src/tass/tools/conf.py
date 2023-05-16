import openpyxl

def convert(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    print("Total row: " + str(ws.max_row))
    print("Total column: " + str(ws.max_column))
