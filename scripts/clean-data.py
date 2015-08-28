import csv
import sys

oldfilename = sys.argv[1]
newfilename = oldfilename + ".clean"

with open(oldfilename, 'rU') as oldfile, open(newfilename, 'w') as newfile:
    reader = csv.reader(oldfile)
    writer = csv.writer(newfile)
    for oldrow in reader:
        newrow = []
        for olditem in oldrow:
            newitem = unicode(olditem, errors="ignore")
            newitem = newitem.strip()
            newitem = " ".join(newitem.split())
            newrow.append(newitem)
        writer.writerow(newrow)
