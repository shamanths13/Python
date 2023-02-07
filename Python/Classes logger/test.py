import json
from datetime import date, timedelta
import os

tdy_date=date.today()
tdy_date_n=tdy_date
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")


with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)

with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)


sheet_date=data_add[-1]['date']
new_date=tdy_date_n.strftime("%d/%m/%Y")
that_day=0
i=0

if new_date != sheet_date:
    with open(os.path.join(os.path.dirname(__file__),"classesdone_backup.json"), 'w') as backup:
            json.dump(data_add, backup, indent = 4)

while new_date != sheet_date:
    new_date=(tdy_date_n-timedelta(days=i+1)).strftime("%d/%m/%Y")    
    i=i+1


new_data = {
    "section": "",
    "cond": "",
    "sch_time": "",
    "act_time": "",
    "hours": "",    
    "lesson": "",
    "remarks": ""
}

for _ in range(i):
    new_date=(tdy_date_n-timedelta(days=i-1)).strftime("%d/%m/%Y")
    that_day=date.weekday(tdy_date_n-timedelta(days=i-1))

    new_day = {
    "date":new_date,
    "day":data[that_day]['day'],
    "classes":[]
}
    with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
        data_add = json.load(f)
        data_add.append(new_day)
        for n, classes in enumerate(data[that_day]['classes']):
            data_add[-1]["classes"].append(new_data)
        f.seek(0)
        json.dump(data_add, f, indent = 4)
        f.truncate()
        for n, classes in enumerate(data[that_day]['classes']):
            with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
                data_add = json.load(f)
                data_add[-1]["classes"][n]["section"]=classes["section"]
                data_add[-1]["classes"][n]["sch_time"]=classes["time"]
                f.seek(0)
                json.dump(data_add, f, indent = 4)
                f.truncate()
    i=i-1




    

