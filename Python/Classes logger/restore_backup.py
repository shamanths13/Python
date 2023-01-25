import os
import json

with open(os.path.join(os.path.dirname(__file__),"classesdone_backup.json"), 'r') as f:
    data = json.load(f)

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'w') as x:
    json.dump(data, x, indent = 4)