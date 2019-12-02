#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from math import floor
import os
from pathlib import Path

class sexeMatrimonial:
    meta = None
    def clean(self):
        self.df.dropna(axis=1,how='all',inplace=True)
        self.df.set_index('Etat Matrimonial',inplace=True)
        self.df.replace(to_replace=',',value='.',regex=True,inplace=True)
        self.df = self.df.astype('int64')
    
    def __init__(self,disabilityType="AllTypes"):
        filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"1_2.csv"
        self.df = pd.read_csv(filePath,index_col=False)
        self.clean()
        self.meta = {"Index":self.df.index.name , "columns":[col for col in self.df.columns],"Disability":disabilityType}
        
    def matrimonial(self):
        return self.df[["Ensemble"]]
    
    def sexeMatrimonial(self):
        return self.df

    def __str__(self):
            return str(self.df)


def main():
    return {disType:sexeMatrimonial(disType) for disType in ["Sensoriel","Chronique","Moteur","Mental"]}

if __name__ == "__main__":
    for df in main():
        print(df)