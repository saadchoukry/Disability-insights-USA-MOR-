import numpy as np
import pandas as pd
import os
from pathlib import Path

class activitySexeEnvirHCP04:
    meta = None
    def clean(self):
        self.df.set_index("Milieu",inplace=True)
        self.df = self.df.astype('float64')


    def __init__(self,disabilityType="AllTypes"):
        filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"4_2.csv"
        self.df = pd.read_csv(filePath,index_col=False)
        self.clean()
        self.meta = {"Index":self.df.index.name , "columns":[col for col in self.df.columns],"Disability":disabilityType}

    def __str__(self):
        return str(self.df)
def main():
    return {disType:activitySexeEnvirHCP04(disType) for disType in ["Sensoriel","Chronique","Moteur","Mental"]}

if __name__ == "__main__":
    main()