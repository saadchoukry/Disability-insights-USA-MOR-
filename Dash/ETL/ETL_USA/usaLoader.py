import pandas as pd 
from pathlib import Path
import os
#from ETL.ETL_USA import myToolz as myToolz 
import ETL.ETL_USA.myToolz as myToolz
class UsaLoader:
    def __init__(self):
        self.dfsArray = []
        rootPath = Path(str(Path(os.path.realpath(__file__)).parent)+"\\dispatchedRessources\\")
        allCsvAbsPaths = list(rootPath.glob('**/*.csv'))
        for csvPath in allCsvAbsPaths:
            newExtendedDf = {'meta':{}}
            csvRelPath = str(csvPath).split('dispatchedRessources\\',maxsplit=1)[1]
            myLoader = myToolz.getDimensionsOptionsStateLoader(csvRelPath,"\\")
            newExtendedDf['meta']["state"] = myLoader["state"]
            myToolz.metaCreator(newExtendedDf,csvRelPath)
            newExtendedDf["dataFrame"] = pd.read_csv(csvPath,index_col=0)
            self.dfsArray.append(newExtendedDf)
            metaPath = Path(str(Path(os.path.realpath(str(csvPath))).parent)+"\\meta.txt")
            dfMeta = myToolz.metaReader(metaPath)
            newExtendedDf['meta']['index'] = dfMeta[0]
            newExtendedDf['meta']['year'] = csvRelPath.split("\\")[1]
            newExtendedDf['meta']['columns'] = dfMeta[1]
            newExtendedDf["dataFrame"].astype('int64',inplace=True)
            """
            if 'EMPLOYMENT SECTOR' in newExtendedDf['meta']['index']:
                print(newExtendedDf['dataFrame'])
            """
            #print(newExtendedDf['meta'])