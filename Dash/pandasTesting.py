from ETL.loader import EtlHcp04
import pandas as pd


init= False
dfs = None
ageSexe04= None
sexeMatri04 = None
def ETL():
    global init,dfs,ageSexe04,sexeMatri04
    if not init :
        print("--- RUNNING ETL ---")
        ETL = EtlHcp04()
        ageSexe04 = ETL.extendedDataFrames[0]
        sexeMatri04 = ETL.extendedDataFrames[1]
    else:
        print("Data has already been loaded")
        return dfs
ETL()

#print(ageSexe04["AllTypes"].df.iloc[3].name == ageSexe04 ["Sensoriel"].df.iloc[3].name)
#print(ageSexe04 ["Sensoriel"].df.iloc[3])
#print(ageSexe04["AllTypes"].df + ageSexe04 ["Sensoriel"].df)


## Sum 2 or more dataframes [Indexes/columns must be the same]
def dfs_sum(dfsArray):
    if len(dfsArray) == 1:
        return dfsArray[0]
    newDf= pd.DataFrame(index=dfsArray[0].index)
    for df in dfsArray:
        newDf = newDf.add(df,fill_value=0)
    return newDf

#print(dfs_sum([ageSexe04["AllTypes"].df,ageSexe04["Sensoriel"].df,ageSexe04["Chronique"].df]))


## Split df into M/F df
def splitMF(df,gender):
    df.drop("Urbain", axis=1, inplace=True)
    df.drop("Rural", axis=1, inplace=True)
    if gender == "M":
        df.drop([5, 6, 7, 8, 9], axis=0, inplace=True)
        df.rename(columns={"Unnamed: 1": "Etat Matrimonial",
                             "Total": "Masculin"}, inplace=True)
    else:
        df.drop([5, 6, 7, 8, 9], axis=0, inplace=True)
        df.rename(columns={"Unnamed: 1": "Etat Matrimonial",
                                 "Total": "Féminin"}, inplace=True)
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df.set_index("Etat Matrimonial", inplace=True)
    return df