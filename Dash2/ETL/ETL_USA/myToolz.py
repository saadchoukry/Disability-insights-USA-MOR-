from re import split as reSplitter
from re import sub as reSubber
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

def usefulColumn(columnName):
    splittedCol = columnName.split('%')
    if "With" in splittedCol[-1]:
        if "No" in splittedCol[-2]:
            return False
        else :
            return True

def usefulColumnCleaner(usefulColumn):
    column = usefulColumn
    if "% With a disability" in usefulColumn:
        usefulColumn= reSubber(r'BY DISABILITY STATUS.*for ','for ',usefulColumn)
        usefulColumn= reSubber(r'% With a disability','',usefulColumn)
        return {column:usefulColumn}
    else:
        return usefulColumn

def dfColRenamer(df,usefulColumns):
    for col in usefulColumns:
        cleaned = usefulColumnCleaner(col)
        if type(cleaned) == dict:
            df.rename(columns=cleaned,inplace=True)




def columnSplitter(columnName):
    splittedColumn = OrderedDict()
    splittedColumn['dimensions'] = [stringCleaner(s) for s in reSplitter('BY | for',columnName.split('%',maxsplit=1)[0])[:-1] ]
    splittedColumn['options'] = [stringCleaner(s) for s in (columnName.split('%',maxsplit=1)[1]).split('%')]
    splittedColumn['dimensions'].append('POPULATION')
    splittedColumn['options'].append(reSplitter('for|%',columnName)[1])
    splittedColumn['rawDimFromRawCol'] = columnName.split("%",maxsplit=1)[0]
    return splittedColumn
"""
print(
    columnSplitter("SEX BY AGE BY DISABILITY STATUS for Civilian Noninstitutionalized Population")
)
"""

def unique(x):
  return list(dict.fromkeys(x))

def getDimOptions(splittedColumns):
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


def routing(remainingDimensions,option,year,dfIndexlabel,dfColumnslabel):
    rootPath = str(Path(os.path.realpath(__file__)).parent) + "\\dispatchedRessources\\year\\"+year+"\\"
    folderName=dfIndexlabel + " BY " + dfColumnslabel
    if not os.path.isdir(rootPath+folderName):
        os.mkdir(rootPath+folderName)
    if not option == " " :    
        folderName += "\\" + option
        if not os.path.isdir(rootPath+folderName):
            os.mkdir(rootPath+folderName)
    return rootPath+folderName

###[('DISABILITY STATUS', ['With a disability', 'No disability']), ('sample', [' Civilian Noninstitutionalized Population'])])


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

def metaWriter(path,index,columns):
    with open(path,'w') as metaFile:
        metaFile.write(str(index))
        metaFile.write('\n')
        metaFile.write(str(columns))
    

def dataFrameCreator(UsaExtTransObject,sample,dfIndex,dfColumns,dimensions,options,index,columns,newColumnsRaw,dfIndexlabel,dfColumnslabel):
    for i in range(len(dimensions)):
        newDf = pd.DataFrame(index=dfIndex , columns=dfColumns)
        for option in options[i]:
            #print(type(option))
            csvPath = routing(dimensions[i],option,UsaExtTransObject.year,dfIndexlabel,dfColumnslabel)
            for state in UsaExtTransObject.dfUs.index:
                for row in newDf.index:
                    for col in newDf.columns:
                        #print(myToolz.columnSelector(newColumnsRaw,row,col,sample,option,dimensions[i]))
                        if dimensions[i] == 'POPULATION':
                            newDf.loc[row][col] = UsaExtTransObject.dfUs.loc[state][columnSelector(newColumnsRaw,row,col,sample,option)]
                            csvCreator(newDf,state,csvPath) 
                        else:
                            newDf.loc[row][col] = UsaExtTransObject.dfUs.loc[state][columnSelector(newColumnsRaw,row,col,sample,option,dimensions[i])]
                            csvCreator(newDf,state,csvPath)
            metaWriter(csvPath+"\\meta.txt",index,columns)   
            #print(csvPath+"\\meta.txt")  


## LOADER
def getDimensionsOptionsStateLoader(relativePath,delimiter):
    path = relativePath
    dimensions = []
    options = []
    counter = 0
    while delimiter in path:
        splittedPath = path.split('\\',maxsplit=1)
        if counter % 2 == 0:
            dimensions.append(splittedPath[0])
        else:
            options.append(splittedPath[0])
        counter +=1
        try:
            path = splittedPath[1]
        except:
            pass

    return {"dimensions":dimensions,"options":options,"state":path.split('.')[0]}

"""
print(
getDimensionsOptionsStateLoader("year\\16\\VISION DIFFICULTY\\With a vision difficulty\\Wyoming.csv","\\")
)  
"""

def metaReader(path):
    meta = []
    with open(path,'r') as metaFile:
        s = metaFile.read().split('\n',maxsplit=1)
    for element in s:
        meta.append(element.split(',',maxsplit=1)[0][2:-1])
    return meta
"""
print(
metaReader("c:\\Users\\Saad\\Desktop\\SAAD\\Stud\\BI\\Projet_BI\\Dash\\ETL\\ETL_USA\\dispatchedRessources\year\\16\\POPULATION\\ Civilian Noninstitutionalized Population For Whom Poverty Status Is Determined\\meta.txt")
)
"""

def metaCreator(ExtendedDf,relativePath):
    meta = {}
    subDirectories = relativePath.split('\\')
    for subDir in subDirectories:
        if "difficulty" in subDir:
            difficulty= ""
            for s in subDir.split(" ")[2:-1]:
                difficulty += s +" " 
            ExtendedDf["meta"]["difficulty"] =difficulty
    return meta
