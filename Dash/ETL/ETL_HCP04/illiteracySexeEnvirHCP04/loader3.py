#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from math import floor
import os
from pathlib import Path
class IllitSexeEnvir:
    meta = None
    def clean(self):
        self.df.dropna(axis=1,how='all',inplace=True)
        self.df.rename(columns={'Unnamed: 0':'Environnement'},inplace=True)
        self.df.set_index('Environnement',inplace=True)
        self.df = self.df.astype('int64')
        
    def __init__(self,disabilityType="AllTypes"):
        self.disabilityType = disabilityType
        filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"3_1.csv"
        self.df = pd.read_csv(filePath,index_col=False)
        self.clean()
        self.meta = {"Index":self.df.index.name , "columns":[col for col in self.df.columns]}
        
    def illitSexe(self):
        return self.df[["Masculin","Féminin"]]
    
    def illitEnvir(self):
        return self.df[["Ensemble"]]
    
    def illitSexeEnvir(self):
        return self.df
    
    def __str__(self):
            return str(self.df)

def main():
    return [IllitSexeEnvir(disType) for disType in ["AllTypes","Sensoriel","Chronique","Moteur","Mental"]]

if __name__ == "__main__":
    for df in main():
        print(df)