import json
from openpyxl import Workbook
from openpyxl.worksheet.filters import (
    FilterColumn,
    CustomFilter,
    CustomFilters,
    DateGroupItem,
    Filters,
    )

wb = Workbook()
ws = wb.active

f = open("path/to/results.json")
with f:
    job = json.load(f)

tr_data = [["Name:", job["name"], "Uuid:", job["uuid"]],
    ["status:", job["status"], "test_start:", job["test_start"]],
    ["Test cases"],
    ["Name", "Uuid", "Status"]]

tr_row_start = len(tr_data)
tr_row_track = len(tr_data)

for case in job["test_cases"]:
    case_report = [case["name"], case["uuid"], case["status"]]
    tr_data.append(case_report)
    tr_row_track += 1
    case_ws = wb.create_sheet(title = case["name"])
    
    case_data = [["Name:", case["name"], "UUID:", case["uuid"], "Status:", case["status"]],
                 ["Steps"],
                 ["Uuid", "Title", "Status"]]
    
    case_row_start = len(case_data)
    case_row_track = len(case_data)

    for step in case["steps"]:
        case_data.append([step["uuid"],step["title"], step["status"]])
        case_row_track += 1
        
    for r in case_data:
        case_ws.append(r)
        
    filter_range = f"A{case_row_start}:C{case_row_track}"
    case_ws.auto_filter.ref = filter_range

for r in tr_data:
    ws.append(r)

# Define filter range (from start cell to last row in that column)
filter_range = f"A{tr_row_start}:C{tr_row_track}"
ws.auto_filter.ref = filter_range

wb.save("quicktest.xlsx")
