import pandas as pd
import os
from pathlib import Path
import json
import re
import myToolz as myToolz
from pprint import pprint

class UsaEtl:
    def cleanSexAge(self):
        rawColumns = []
        WithColumns = []
        WithoutColumns = []
        ## Dimensions container
        workingSheet = myToolz.splitter(self.dfUs16.columns[1])["dimensionsRaw"]
        for col in self.dfUs16.columns:
            ## Grouping columns with the same dimensions
            if workingSheet in col:
                newCol = myToolz.splitter(col)['disability']
                if 'No disability' in newCol :
                    WithoutColumns.append(newCol)
                else:
                    WithColumns.append(newCol)
                rawColumns.append(col)
        #pprint(rawColumns)
        #dimOptions = myToolz.dataFrameCreator(columns)
        """
        for state in self.dfUs16.index:
            df = pd.DataFrame(index=dimOptions['AGE'] , columns=dimOptions['SEX'])
            for row in df.index:
                for col in df.columns:
                    df.loc[row][col] = self.dfUs16.loc[state][myToolz.columnSelector(rawColumns,row,col,"With a disability")]
       """
        

    def __init__(self):
        
        dataPath = str(Path(os.path.realpath(__file__)).parent) + "\\USA_All_States.csv"
        jsonPath = str(Path(os.path.realpath(__file__)).parent) + "\\03_ColumnKey.json"
        with open(jsonPath, "r") as read_file:
            dataColNames = json.load(read_file)
        newColNames = {}
        for col in dataColNames:
            #print(col["description"])
            newColNames[col["columnname"]] = col["description"] 
        self.dfUs16 = pd.read_csv(dataPath)
        self.dfUs16.drop(columns=["SummaryLevel","StateFIPS","GEOID",],axis=1,inplace=True)
        self.dfUs16 = self.dfUs16.rename(columns=newColNames)
        self.dfUs16.set_index("AreaName",inplace=True)

        ## Eliminating columns containing totals/sub-totals
        noTotalColumns= []
        for col in self.dfUs16.columns:
            if col.count("BY")+1 ==  col.count("%"):
                 noTotalColumns.append(col)
        self.dfUs16 = self.dfUs16[noTotalColumns]

        self.cleanSexAge()
    
 

UsaEtl()

