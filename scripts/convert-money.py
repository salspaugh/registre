import csv
import sys

IDX = 15

oldfilename = sys.argv[1]
newfilename = oldfilename + ".clean"

with open(oldfilename, 'rU') as oldfile, open(newfilename, 'w') as newfile:
    reader = csv.reader(oldfile)
    writer = csv.writer(newfile)
    header = True
    for oldrow in reader:
        if header: 
            header = False
            writer.writerow(oldrow)
            continue
        money = oldrow[IDX]
        money = money.replace("$", "").replace(",", "")
        if money[0] == "(" and money[-1] == ")":
            money = money.replace("(", "-").replace(")", "")
        money = float(money)
        newrow = oldrow
        newrow[IDX] = money
        writer.writerow(newrow)
