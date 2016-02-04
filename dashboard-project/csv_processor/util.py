"""
A utility module for use in other files.
"""

import csv,codecs,cStringIO, json
from datetime import datetime

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")
    
class UnicodeReader:
    """
    A type of CSV Reader that supports Unicode values in CSV files.
    Not required if using Python 3, but is for Python 2.
    """
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8", errors="replace") for s in row]
    def __iter__(self):
        return self
    
class DatetimeEncoder(json.JSONEncoder):
    """
    A type of JSONEncoder that knows how to handle date and datetime
    objects. Serialises to a standard ISO format, which is 
    usable directly in JS.
    """
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)