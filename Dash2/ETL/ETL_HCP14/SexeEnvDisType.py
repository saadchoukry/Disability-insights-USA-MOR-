import numpy as np
import pandas as pd
import os
from pathlib import Path


class SexeEnvDisType_HCP14:
    def __init__(self,disabilityType="AllTypes"):
        self.dfsArray = []
        rootPath = Path(str(Path(os.path.realpath(__file__)).parent)+"\\Ressources_HCP14\\")
        allCsvAbsPaths = list(rootPath.glob('**/*.csv'))
        for csvPath in allCsvAbsPaths:
            newExtendedDf = {'meta':{}}
            csvRelPath = str(csvPath).split('Ressources_HCP14\\',maxsplit=1)[1]
            newExtendedDf['meta']['disType'] = csvRelPath.split("\\")[0]
            newExtendedDf['meta']['env'] = csvRelPath.split("\\")[1].split(".")[0]
            newExtendedDf['dataFrame'] = pd.read_csv(csvPath,index_col=0)
            self.dfsArray.append(newExtendedDf)
          
            
    def __str__(self):
        return str(self.dfsArray)
