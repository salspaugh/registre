import collections
import csv
import inspect
import json

class DataType(object):
    
    INTEGER = "int"
    FLOAT = "float"
    STRING = "str"

CASTS = {
    DataType.INTEGER: int,
    DataType.FLOAT: float,
    DataType.STRING: str
}

class Scale(object):

    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    QUANTITATIVE = "quantitative"

class SemanticType(object):
    
    BINARY = "binary"
    COUNT = "count"
    LABEL = "label"     
    TEXT = "text"
    MONEY = "money"
    CITY = "city" # geographic
    COUNTY = "county"
    STATE = "state"
    COUNTRY = "country"
    TIMEOFDAY = "timeofday" # time
    DAYOFWEEK = "dayofweek"
    DAYOFMONTH = "dayofmonth"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    DATE = "date"

def get_attribute_values(klass):
    attrs = inspect.getmembers(klass, lambda a:not(inspect.isroutine(a)))
    return [a[1] for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]

VALID_DATA_TYPES = get_attribute_values(DataType)
VALID_SCALES = get_attribute_values(Scale)
VALID_SEMANTIC_TYPES = get_attribute_values(SemanticType)

class DatasetMetadata(object):
    
    def __init__(self):
        self.name = ""
        self.columns = {}

    def jsonify(self):
        d = {}
        d['name'] = self.name
        d['columns'] = { name: col.jsonify() for (name, col) in self.columns.iteritems() }
        return d

class ColumnMetadata(object):

    def __init__(self, name):
        self.name = name
        self.domain = None
        self.scale = ""
        self.datatype = ""
        self.semantictype = ""

    def jsonify(self):
        return self.__dict__

def generate_metadata(csvfile, typesfile=None, inferdomain=False):
    colvals = collections.defaultdict(list)
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        for (colname, colval) in row.iteritems():
            if colname == "": continue
            colvals[colname].append(colval)
    columns = {}
    column_data = None
    if typesfile is not None:
        types = json.load(typesfile)
        column_data = types["columns"]
    for (name, values) in colvals.iteritems():
        c = ColumnMetadata(name)
        if column_data is not None:
            c.__dict__.update(column_data.get(name, {}))
            check_validity(c)
        if inferdomain:
            infer_domain(c, values)
        columns[c.name] = c
    d = DatasetMetadata()
    d.name = csvfile.name.split('.')[0]
    d.columns = columns
    return d

def check_validity(column):
    try:
        assert column.datatype in VALID_DATA_TYPES
    except:
        msg = "Bad data type %s for column %s" % (column.datatype, column.name)
        raise AssertionError(msg)
    try:
        assert column.semantictype in VALID_SEMANTIC_TYPES
    except:
        msg = "Bad semantic type %s for column %s" % (column.semantictype, column.name)
        raise AssertionError(msg)
    try:
        assert column.scale in VALID_SCALES
    except:
        msg = "Bad scale %s for column %s" % (column.scale, column.name)
        raise AssertionError(msg)

def infer_domain(column, values):
    none = False
    cast_values = []
    for v in values:
        if v == "" and not column.datatype == DataType.STRING:
            none = True
        else:
            v = cast_value(v, column)
            cast_values.append(v)
    if column.scale == Scale.NOMINAL or column.scale == Scale.ORDINAL:
        column.domain = list(set(cast_values))
        column.domain.sort()
    if column.scale == Scale.QUANTITATIVE:
        column.domain = {
            "max": max(cast_values) if len(cast_values) > 0 else None,
            "min": min(cast_values) if len(cast_values) > 0 else None,
            "cardinality": len(set(cast_values))
        }
        if none:
            column.domain["none"] = ""

def cast_value(v, column):
    try:
        if column.datatype == DataType.INTEGER:
            v = float(v) # e.g., 1.00 fails to cast to int
        if column.datatype == DataType.STRING:
            v = unicode(v, errors="ignore") 
        v = CASTS[column.datatype](v)
    except Exception as e:
        print "Error casting value."
        print e
        print column.name, column.datatype, v
    return v

def output_metadata(metadata, outputfilename):
    with open(outputfilename, 'w') as outputfile:
        json.dump(metadata.jsonify(), outputfile, sort_keys=True, indent=4, separators=(',', ': '))
