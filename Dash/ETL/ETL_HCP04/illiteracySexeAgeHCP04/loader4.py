

import pandas as pd
import numpy as np
from math import floor
import os 
from pathlib import Path

class IllitSexeAge:
    meta = None
    def clean(self):
        self.df.set_index('groupes d’âges',inplace=True)
        self.df = self.df.astype('int64')
        
        
    def __init__(self,disabilityType="AllTypes"):
        filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"3_2.csv"
        self.df = pd.read_csv(filePath,index_col=False)
        self.clean()
        self.meta = {"Index":self.df.index.name , "columns":[col for col in self.df.columns],"Disability":disabilityType}
        
    def IllitAge(self):
        return self.df[["Ensemble"]]
    
    def IllitSexeAge(self):
        return self.df
        
    def __str__(self):
            return str(self.df)

def main():
    return {disType:IllitSexeAge(disType) for disType in ["Sensoriel","Chronique","Moteur","Mental"]}

if __name__ == "__main__":
    main()
        