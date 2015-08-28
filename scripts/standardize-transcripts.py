import csv
import json
import sys

# anna-cameron
#filename = sys.argv[1]
#data = []
#with open(filename) as f:
#    reader = csv.DictReader(f, delimiter="\t")
#    for row in reader:
#        item = {
#            "raw_time": row["Time"],
#            "goal": row["Goal (Why)"],
#            "action": row["Actions (What)"],
#            "interpretation": row["Result"]
#        }
#        data.append(item)
#
#with open("output.json", "w") as f:
#    json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

# pablo-sophia
#filename = sys.argv[1]
#data = []
#with open(filename, "rU") as f:
#    reader = csv.DictReader(f)
#    for idx, row in enumerate(reader):
#        item = {
#            "screenshot": "screenshot-%d.png" % idx,
#            "goal": row["Goal"],
#            "action": row["Action"],
#            "interpretation": row["Interpretation/Question"]
#        }
#        data.append(item)
#
#with open("output.json", "w") as f:
#    json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

# hassan-shubham
#filename = sys.argv[1]
#data = []
#last = None
#step_count = 0
#with open(filename, "rU") as f:
#    for line in f.readlines():
#        print line
#        line = line.strip().encode("utf8")
#        if line == "":
#            continue
#        if line.find("Step") > -1:
#            rparen_idx = line.find("(")
#            lparen_idx = line.find(")")
#            datetime = line[rparen_idx+1:lparen_idx]
#            date = datetime.split()[0]
#            time = " ".join(datetime.split()[1:])
#            action = line[lparen_idx+1:]
#            item = {
#                "screenshot": "screenshot-%d.png" % step_count,
#                "raw_time": time,
#                "raw_date": date,
#                "action": action,
#            }
#            last = item
#            data.append(item)
#            step_count += 1
#        if line.find("Comment") > -1:
#            last["goal"] = line
#        if line.find("No screenshots were saved") > -1:
#            del last["screenshot"]
#
#with open("output.json", "w") as f:
#    json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

# taek-shaun
filename = sys.argv[1]
data = []
curr = {}
with open(filename, "rU") as f:
    for line in f.readlines():
        line = line.strip().encode("utf8")
        if line == "":
            if len(curr) > 0:
                data.append(curr)
            curr = {}
            continue
        if line.find("Time-check:") == 0:
            line = line.split(":")
            time = ":".join(line[1:]).strip()
            curr["raw_time"] = time 
        elif line.find("Doing:") == 0:
            curr["action"] = line
        elif line.find("Why-doing:") == 0:
            curr["goal"] = line
        elif line.find("Interpretation:") == 0:
            curr["interpretation"] = line

with open("output.json", "w") as f:
    json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
