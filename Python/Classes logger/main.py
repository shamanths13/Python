import json

with open('schedule.json') as f:
    data = json.load(f)

print(data['day'])