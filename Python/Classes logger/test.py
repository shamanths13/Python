import json
from datetime import date
import os

tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")
print(tdy_date)

new_day = {
    "day":tdy_date,
    "classes":[]
}

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)
    print(len(data_add))
    if data_add[-1]['day'] != tdy_date:
        data_add.append(new_day)
        f.seek(0)
        json.dump(data_add, f, indent = 4)


    

