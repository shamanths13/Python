import json
from datetime import date
import os

tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")
print(tdy_date)


with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)

new_day = {
    "date":tdy_date,
    "day":data[tdy_day]['day'],
    "classes":[]
}

new_data = {
    "section": "",
    "cond_remarks": "",
    "sch_time": "",
    "act_time": "",
    "hours": "",    
    "lesson": ""
}

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)
    print(len(data_add))
    data_add.append(new_day)
    f.seek(0)
    json.dump(data_add, f, indent = 4)

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)
    data_add[len(data_add)-1]["classes"].append(new_data)
    f.seek(0)
    json.dump(data_add, f, indent = 4)


print(data[0]['classes'][1]['section'])
for n, classes in enumerate(data[tdy_day]['classes']):
    print(classes['section'],"Time: ", classes['time'])
    

