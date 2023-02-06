from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment
import os
import json

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r') as f:
    data = json.load(f)

wb=Workbook()
ws=wb.active

row=1

for n,day in enumerate(data):
    ws['A'+str(row)].value=data[n]["day"]
    ws['A'+str(row)].font=Font(bold=True, size=12 )
    ws['A'+str(row)].alignment=Alignment(vertical='center', horizontal='center')
    ws['B'+str(row)].value=data[n]["date"]
    ws['B'+str(row)].font=Font(bold=True, size=12 )
    ws['B'+str(row)].alignment=Alignment(vertical='center', horizontal='center')
    m=0
    if len(data[n]["classes"]) > 0:
        for m,session in enumerate(data[n]["classes"]):
            ws['C'+str(row+m)].value=session["section"]
            ws['D'+str(row+m)].value=session["cond"]
            ws['E'+str(row+m)].value=session["sch_time"]
            ws['F'+str(row+m)].value=session["act_time"]
            ws['G'+str(row+m)].value=session["hours"]
            if session["hours"] != "  Hours  ":
                if session["hours"]!= "":
                    hrs_red=session["hours"].split(":")
                    hrs_red=round((int(hrs_red[0])+(int(hrs_red[1])/60)),3)
                    ws['H'+str(row+m)].value=str(hrs_red)
            else:
                ws['H'+str(row+m)].value="  Hours Conv  "
            ws['I'+str(row+m)].value=session["lesson"]
            ws['J'+str(row+m)].value=session["remarks"]
    ws.merge_cells("A"+str(row)+":"+"A"+str(row+m))
    ws.merge_cells("B"+str(row)+":"+"B"+str(row+m))
    row=row+m+2

for col in range(1, 11):
    ws[get_column_letter(col)+'1'].font=Font(bold=True, size=12 )
    ws.column_dimensions[get_column_letter(col)].width = len(ws[get_column_letter(col)+'1'].value)*1.1
    ws[get_column_letter(col)+'1'].alignment=Alignment(horizontal='center')

wb.save(os.path.join(os.path.dirname(__file__),"CompletedClasses.xlsx"))

