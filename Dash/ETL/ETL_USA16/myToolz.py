from re import split as reSplitter
from pprint import pprint
import numpy as np
def stringCleaner(s):
    if s[0:1] == ' ':
        s = s[1:]  
    if s[-1] == ':' or s[-1] == ' ':
        s = s[:-1]
    return s

def splitter(columnName):
    sample = reSplitter('for|%',columnName)[1]
    disability = stringCleaner(columnName.split('%')[-1])
    options = [stringCleaner(s) for s in (columnName.split('%',maxsplit=1)[1]).split('%')[:-1]]
    dimensions = [stringCleaner(s) for s in reSplitter('BY | for',columnName.split('%',maxsplit=1)[0])[:-2] ]
    return {
        'sample':sample ,
        'disability':disability,
        'options':options,
        'dimensions':dimensions,
        'dimensionsRaw':columnName.split("for",maxsplit=1)[0]
        }

def unique(x):
  return list(dict.fromkeys(x))

def dataFrameCreator(splittedColumns):
    dikt = {s:[] for s in splittedColumns[0]['dimensions']}
    for col in splittedColumns:
        for i in range(len(col['dimensions'])):
            try:
                dikt[col['dimensions'][i]] = unique(dikt[col['dimensions'][i]] + [col['options'][i]])
            except:
                pass
    return dikt


def columnSelector(columns,*stringsToCheck):
    exists = 0
    for col in columns:
        for s in stringsToCheck:
            if s in col:
                exists += 1
        if exists == len(stringsToCheck):
            return col
        else:
            exists = 0
    return False

