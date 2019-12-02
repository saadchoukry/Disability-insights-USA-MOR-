import numpy as np
import pandas as pd
import os
from pathlib import Path

class EducationEnvirHCP04:
        meta = None
        def clean(self):
            self.df.set_index('Niveaux d’études',inplace=True)
            try:
                self.df.drop(["ND"],axis=0,inplace=True)
            except:
                pass
            self.df.replace(to_replace=',',value='.',regex=True,inplace=True)
            self.df = self.df.astype('int64')  
    
        def __init__(self,disabilityType="AllTypes"):
            filePath = str(Path(os.path.realpath(__file__)).parent.parent) + "\\Ressources\\"+disabilityType+"3_3.csv"
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
        
        def __str__(self):
            return str(self.df)
def main():
    return {disType:EducationEnvirHCP04(disType) for disType in ["Sensoriel","Moteur","Mental","Chronique"]}

if __name__ == "__main__":
    main()