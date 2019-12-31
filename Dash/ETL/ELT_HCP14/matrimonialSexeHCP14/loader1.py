import pandas as pd
import os
from pathlib import Path



class sexeMatrimonial:
    meta = None


    def clean(self,filename):
        ultiPath = str(Path(os.path.realpath(__file__)).parent.parent)
        filePath = ultiPath + "\\Ressources\\"+ filename + ".csv"
        self.df = pd.read_csv(filePath)
        self.df.replace(to_replace=' ', value='', regex=True, inplace=True)
        self.df = self.df.astype({'Urbain': 'int64', 'Rural': 'int64', 'Total': 'int64'})
        self.dfM = self.splitMF(self.df,"M")
        self.dfF = self.splitMF(self.df,"F")

        print(self.dfM)
        print(self.dfF)




    def __init__(self):
        pass


sexeMatrimonial().clean("matrimonialSexeHCP14")