from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment
import os
import json

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r') as f:
    data = json.load(f)

wb=Workbook()
ws=wb.active


print(data[1]["date"])

row=1

for n,day in enumerate(data):
    ws['A'+str(row)].value=data[n]["day"]
    ws['A'+str(row)].font=Font(bold=True, size=12 )
    ws['A'+str(row)].alignment=Alignment(vertical='center', horizontal='center')
    ws['B'+str(row)].value=data[n]["date"]
    ws['B'+str(row)].font=Font(bold=True, size=12 )
    ws['B'+str(row)].alignment=Alignment(vertical='center', horizontal='center')
    for m,session in enumerate(data[n]["classes"]):
        ws['C'+str(row+m)].value=session["section"]
        ws['D'+str(row+m)].value=session["cond_remarks"]
        ws['E'+str(row+m)].value=session["sch_time"]
        ws['F'+str(row+m)].value=session["act_time"]
        ws['G'+str(row+m)].value=session["hours"]
        ws['H'+str(row+m)].value=session["lesson"]
    ws.merge_cells("A"+str(row)+":"+"A"+str(row+m))
    ws.merge_cells("B"+str(row)+":"+"B"+str(row+m))
    row=row+len(data[n]["classes"])+1

for col in range(1, 9):
    ws[get_column_letter(col)+'1'].font=Font(bold=True, size=12 )
    ws.column_dimensions[get_column_letter(col)].width = len(ws[get_column_letter(col)+'1'].value)

wb.save(os.path.join(os.path.dirname(__file__),"CompletedClasses.xlsx"))
