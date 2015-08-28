import collections
import csv
import sys

def read_columns(datafilename):
    with open(datafilename, 'rU') as datafile:
        reader = csv.DictReader(datafile)
        columns = collections.defaultdict(list)
        for row in reader:
            for (name, val) in row.iteritems():
                columns[name].append(val)
        return columns

def print_values(values):
    values = list(set(values))
    values.sort()
    for v in values:
        print v

def get_user_input(columns):
    while True:
        msg = "\nEnter a column name: "
        input  = raw_input(msg)
        values = columns.get(input, None)
        if values is None:
            print "No column by that name."
        else:
            print_values(values)

datafilename = sys.argv[1]
columns = read_columns(datafilename)
get_user_input(columns)

