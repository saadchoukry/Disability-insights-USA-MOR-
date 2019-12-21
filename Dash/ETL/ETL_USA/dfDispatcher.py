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
            workingSheet = myToolz.columnSplitter(self.dfUs.columns[1])["rawColumn"]
            for col in self.dfUs.columns:
                ## Grouping columns with the same dimensions
                if workingSheet in col:
                    newCol = myToolz.columnSplitter(col)
                    newColumns.append(newCol)
                    newColumnsRaw.append(col)
            dimOptions = myToolz.dataFrameCreator(newColumns)
            sample = newColumns[0]['options'][-1]
            dfIndex = list(dimOptions.popitem(last=False)[-1])
            dfColumns = list(dimOptions.popitem(last=False)[-1])
            while len(dimOptions)> 0 :
                remainingDimsOpts =myToolz.getDimensionsOptions(dimOptions)
                dimensions = remainingDimsOpts['dimensions']
                options = remainingDimsOpts['options']
                for i in range(len(dimensions)):
                    newDf = pd.DataFrame(index=dfIndex , columns=dfColumns)
                    for option in options[i]:
                        csvPath = myToolz.routing(dimensions[i],option,self.year)
                        for state in self.dfUs.index:
                            for row in newDf.index:
                                for col in newDf.columns:
                                    #print(myToolz.columnSelector(newColumnsRaw,row,col,sample,option,dimensions[i]))
                                    if dimensions[i] == 'POPULATION':
                                        newDf.loc[row][col] = self.dfUs.loc[state][myToolz.columnSelector(newColumnsRaw,row,col,sample,option)]
                                        myToolz.csvCreator(newDf,state,csvPath) 
                                    else:
                                        newDf.loc[row][col] = self.dfUs.loc[state][myToolz.columnSelector(newColumnsRaw,row,col,sample,option,dimensions[i])]
                                        myToolz.csvCreator(newDf,state,csvPath)
                print(newDf)
                        
                                                
                    
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
        noTotalColumns= []
        for col in self.dfUs.columns:
            if col.count("BY")+1 ==  col.count("%"):
                 noTotalColumns.append(col)
        self.dfUs = self.dfUs[noTotalColumns]
        self.dispatcher()
    
 
