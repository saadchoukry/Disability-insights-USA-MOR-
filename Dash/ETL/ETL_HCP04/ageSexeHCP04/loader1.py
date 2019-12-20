#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
from pathlib import Path

class AgeSexeTypeHCP04:
        meta = None
        def clean(self):
            self.df.drop(columns='0',axis=1,inplace=True)
            self.df.columns = [col.replace("\r"," ") for col in self.df.columns]
            self.df.dropna(axis=1,how='all',inplace=True)
            self.df.rename(columns={'Unnamed: 2':'Masculin','Unnamed: 4':'Ensemble','Effectifs':'Féminin','groupes d’âges':"groupes d'âges"},inplace=True)
            self.df.at[16,"groupes d'âges"]="75+"
            self.df.set_index("groupes d'âges",inplace=True)
            self.df.drop(axis=0,index=np.NaN,inplace=True)
            self.df.replace(to_replace=' ',value='',regex=True,inplace=True)
            self.df = self.df.astype({'Masculin':'int64','Féminin':'int64','Ensemble':'int64'})        
    
        def __init__(self,disabilityType="AllTypes"):
            filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"1_1.csv"
            self.df = pd.read_csv(filePath,index_col=False)
            self.clean()
            self.meta = {"Index":self.df.index.name , "columns":[col for col in self.df.columns],"Disability":disabilityType}

        def sexe(self):
            prevalence = pd.DataFrame(columns=["Prévalence","Sexe"],dtype='int64')
            prevalence=prevalence.append({'Sexe' : 'Masculin' , 'Prévalence' : np.NaN},ignore_index=True)
            prevalence=prevalence.append({'Sexe' : 'Féminin' , 'Prévalence' : np.NaN},ignore_index=True)
            prevalence.at[0,"Prévalence"] = self.df["Masculin"].sum()
            prevalence.at[1,"Prévalence"] = self.df["Féminin"].sum()
            return prevalence.astype({'Prévalence':'int64'})
        
        def age(self):
            return self.df[["Ensemble"]]
        
        def sexeAge(self):
            return self.df

        def __str__(self):
            return str(self.df)
def main():
    return {disType:AgeSexeTypeHCP04(disType) for disType in ["Sensoriel","Chronique","Moteur","Mental"]}

if __name__ == "__main__":
    for r in main().values():
        print(r)