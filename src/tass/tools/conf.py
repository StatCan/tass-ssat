import openpyxl

def convert(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    print("Total row: " + ws.max_row)
    print("Total column: " + ws.max_column)
