import pandas as pd 
from pathlib import Path
import os
import myToolz as myToolz 

class UsaLoader:
    def __init__(self):
        self.dfsArray = []
        rootPath = Path(str(Path(os.path.realpath(__file__)).parent)+"\\dispatchedRessources\\")
        allCsvAbsPaths = list(rootPath.glob('**/*.csv'))
        for csvPath in allCsvAbsPaths:
            newExtendedDf = {'meta':{}}
            csvRelPath = str(csvPath).split('dispatchedRessources\\',maxsplit=1)[1]
            myLoader = myToolz.getDimensionsOptionsStateLoader(csvRelPath,"\\")
            dimensions = myLoader["dimensions"]
            options = myLoader["options"]
            newExtendedDf['meta']["state"] = myLoader["state"]
            for i in range(len(dimensions)):
                newExtendedDf['meta'][dimensions[i]] = options[i]
            newExtendedDf["dataFrame"] = pd.read_csv(csvPath,index_col=0)
            self.dfsArray.append(newExtendedDf)
            metaPath = Path(str(Path(os.path.realpath(str(csvPath))).parent)+"\\meta.txt")
            dfMeta = myToolz.metaReader(metaPath)
            newExtendedDf['meta']['index'] = dfMeta[0]
            newExtendedDf['meta']['columns'] = dfMeta[1]


UsaLoader()