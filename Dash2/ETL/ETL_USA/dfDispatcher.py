import pandas as pd
import os
from pathlib import Path
import json
import re
import myToolz as myToolz
from pprint import pprint
from collections import Counter, OrderedDict


class UsaExtractTransform:
    def dispatcher(self):
        ## Dimensions container
        while len(self.dfUs.columns) > 0 :
            newColumns = []
            newColumnsRaw = []
            workingSheet = myToolz.columnSplitter(self.dfUs.columns[1])
            for col in self.dfUs.columns:
                ## Grouping columns with the same dimensions
                if workingSheet["rawDimFromRawCol"] in col:
                    newCol = myToolz.columnSplitter(col)
                    newColumns.append(newCol)
                    newColumnsRaw.append(col)
            dimOptions = myToolz.getDimOptions(newColumns)
            #print(dimOptions)
            sample = newColumns[0]['options'][-1]

            index = list(dimOptions.popitem(last=False))
            columns = list(dimOptions.popitem(last=False))

            dfIndex = index[-1]
            dfColumns = columns[-1]

            remainingDimsOpts =myToolz.getDimensionsOptions(dimOptions)
            print(remainingDimsOpts)
            dimensions = remainingDimsOpts['dimensions']
            dimensions.insert(0,index[0])

            options = remainingDimsOpts['options']
            options.insert(0," ")

        
            myToolz.dataFrameCreator(self,sample,dfIndex,dfColumns,dimensions,options,index,columns,newColumnsRaw,index[0],columns[0])
            
            self.dfUs = self.dfUs.drop(columns =newColumnsRaw ,axis=1)       
            
            
          
            
    def __init__(self,year):
        dataPath = str(Path(os.path.realpath(__file__)).parent) + "\\rawRessources\\USA_All_States_"+year+".csv"
        jsonPath = str(Path(os.path.realpath(__file__)).parent) + "\\rawRessources\\columnsIdentification.json"
        with open(jsonPath, "r") as read_file:
            dataColNames = json.load(read_file)
        newColNames = {}
        for col in dataColNames:
            newColNames[col["columnname"]] = col["description"] 
        self.year = year
        self.dfUs = pd.read_csv(dataPath)
        self.dfUs.drop(columns=["SummaryLevel","StateFIPS","GEOID",],axis=1,inplace=True)
        self.dfUs = self.dfUs.rename(columns=newColNames)
        self.dfUs.set_index("AreaName",inplace=True)

        ## Eliminating columns containing totals/sub-totals
        usefulColumns= []
        for col in self.dfUs.columns:
            if col.count("BY")+1 ==  col.count("%") and myToolz.usefulColumn(col):
                 usefulColumns.append(col)
        self.dfUs = self.dfUs[usefulColumns]
        myToolz.dfColRenamer(self.dfUs,usefulColumns)
        #pprint(self.dfUs.columns)
        #pprint(usefulColumns)
        
    
 
