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