from ETL.loader import EtlHcp04
import pandas as pd

## Sum 2 or more dataframes [Indexes/columns must be the same]
def dfs_sum(dfsArray):
    if len(dfsArray) == 1:
        return dfsArray[0]
    newDf= pd.DataFrame(index=dfsArray[0].index)
    for df in dfsArray:
        newDf = newDf.add(df,fill_value=0)
    return newDf
