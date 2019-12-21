from re import split as reSplitter
from pprint import pprint
import numpy as np
from collections import OrderedDict
from pathlib import Path
import os
import pandas as pd

def stringCleaner(s):
    if s[0:1] == ' ':
        s = s[1:]  
    if s[-1] == ':' or s[-1] == ' ':
        s = s[:-1]
    return s

def columnSplitter(columnName):
    splittedColumn = OrderedDict()
    splittedColumn['dimensions'] = [stringCleaner(s) for s in reSplitter('BY | for',columnName.split('%',maxsplit=1)[0])[:-1] ]
    splittedColumn['options'] = [stringCleaner(s) for s in (columnName.split('%',maxsplit=1)[1]).split('%')]
    splittedColumn['dimensions'].append('POPULATION')
    splittedColumn['options'].append(reSplitter('for|%',columnName)[1])
    splittedColumn['rawColumn'] = columnName.split("%",maxsplit=1)[0]
    return splittedColumn


def unique(x):
  return list(dict.fromkeys(x))

def dataFrameCreator(splittedColumns):
    dikt = OrderedDict()
    for s in splittedColumns[0]['dimensions']:
        dikt[s] = []
    for col in splittedColumns:
        for i in range(len(col['dimensions'])):
            try:
                dikt[col['dimensions'][i]] = unique(dikt[col['dimensions'][i]] + [col['options'][i]])
            except:
                pass
    return dikt
"""
print(dataFrameCreator([columnSplitter(s) for s in ["SEX BY AGE BY DISABILITY STATUS for Civilian Noninstitutionalized Population% Male:% Under 5 years:% With a disability",
"SEX BY AGE BY DISABILITY STATUS for Civilian Noninstitutionalized Population% Male:% Under 5 years:% No disability",
"SEX BY AGE BY DISABILITY STATUS for Civilian Noninstitutionalized Population% Female% 5 to 17 years:% With a disability",
"SEX BY AGE BY DISABILITY STATUS for Non civilian hispanic motherfucker% Male:% 5 to 17 years:% No disability",
]]))
"""



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


def routing(dimension,option,year):
    rootPath = str(Path(os.path.realpath(__file__)).parent) + "\\dispatchedRessources\\"+year+"\\"
    folderName=dimension
    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)
    folderName += "\\" + option
    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)
    return rootPath+folderName

###[('DISABILITY STATUS', ['With a disability', 'No disability']), ('sample', [' Civilian Noninstitutionalized Population'])])

def folderCreator(dimensions,sample,disability):
    rootPath = str(Path(os.path.realpath(__file__)).parent) + "\\Ressources\\"
    ## NESTING LVL 1 
    folderName = dimensions[0]
    for dimension in dimensions[1:]:
        folderName +=" BY "+ dimension

    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)


    ## NESTING LVL 2
    folderName +="\\" +  sample
    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)


    ## NESTING LVL 3
    if "No disability" == disability or "With a disability" == disability:
        folderName += "\\General"
        if not os.path.isdir(rootPath+folderName):
            os.mkdir(rootPath+folderName)
    else:                
        folderName += "\\Specific"
        if not os.path.isdir(rootPath+folderName):
            os.mkdir(rootPath+folderName)        

    ## NESTING LVL 4
    folderName +="\\" +  disability
    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)
    
    return rootPath+folderName


def csvCreator(df,state,path):
    csvfileName = path + "\\"+ state + ".csv"
    df.to_csv(csvfileName)
"""
pprint(
    splitter("AGE BY DISABILITY STATUS (WHITE ALONE) for White Alone Civilian Noninstitutionalized Population% Under 18 years:% With a disability")
)
#AGE BY DISABILITY STATUS (WHITE ALONE) for White Alone Civilian Noninstitutionalized Population% Under 18 years:% With a disability

"""

# EMPLOYMENT TYPE
# BY
# EMPLOYEMENT STATUS 
# BY 
# DISABILITY STATUS 
# for 
# Civilian Noninstitutionalized Population 18 To 64 Years
# % In the labor force:
# % Unemployed:
# % With a disability"




def getDimensionsOptions(dimOptions):
    dimensions = []
    options = []
    while len(dimOptions) > 0:
        item = dimOptions.popitem(last=False) 
        dimensions.append(item[0])
        options.append(item[1])
    return {'dimensions':dimensions,'options':options}