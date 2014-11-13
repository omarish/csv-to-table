# TODO: memoize.
# TODO: use namedtuple instead of magic string.

from dateutil import parser as dateParser
import random
import csv
from collections import defaultdict

def is_boolean(s):
    return s.lower() in ['true', 'false', 't', 'f', '0', '1']

def is_date(s):
    try:
        dt = dateParser.parse(s)
        return (dt.hour, dt.minute, dt.second) == (0, 0, 0)
    except:
        return False

def is_timestamp(s):
    try:
        dateParser.parse(s)
        return True
    except:
        return False

def is_numeric(s):
    try:
        float(s)
        return True
    except:
        return False

def is_integer(s):
    try:
        a = float(s)
        n = int(a)

        return a == n
    except:
        return False

def guess_type(s):
    if not s or s == '':
        return None
    elif is_boolean(s):
        return "boolean"
    elif is_integer(s):
        return "integer"
    elif is_numeric(s):
        return "numeric"
    elif is_date(s):
        return "date"
    elif is_timestamp(s):
        return "timestamp"
    else:
        return "string"

class Processor:
    def __init__(self, f, has_header=True):
        self.f = f
        self.reader = csv.reader(self.f)
        if has_header:
            self.header = next(self.reader)
        else:
            self.header = ["row_%i" % x for x in range(len(next(self.reader)))]
            self.f.seek(0)
        self.rows = [[] for x in self.header]

    def add_row(self, row):
        for i, elem in enumerate(row):
            type = guess_type(elem)
            if type:
                self.rows[i].append(type)

    def process_csv(self, sample_probability=0.50):
        for row in self.reader:
            if random.random() <= sample_probability:
                self.add_row(row)
        row_types = self.determine_row_types()

    def determine_col_type(self, col):
        if 'string' in col:
            return 'string'
        elif all([x == 'boolean' for x in col]):
            return 'boolean'
        elif ('integer' in col) and ('boolean' in col) and 'numeric' not in col:
            return 'integer'
        elif ('numeric' in col) and ('boolean' in col):
            return 'numeric'
        else:
            for t in ('boolen', 'integer', 'numeric', 'timestamp', 'date'):
                if all([x == t for x in col]):
                    return t
            return 'string'

    def determine_row_types(self):
        return zip(self.header, [self.determine_col_type(col) for col in
            self.rows])

sql_mappings = {
  'string': 'character varying'
}

def sql_type(x):
    if x in sql_mappings:
        r = sql_mappings[x]
    else:
        r = x
    return r.upper()

def map_sql(table_name, d):
    return "CREATE TABLE " + table_name + " (" + \
            ",".join(["%s %s" % (c, sql_type(t)) for c,t in d]) + ");"
