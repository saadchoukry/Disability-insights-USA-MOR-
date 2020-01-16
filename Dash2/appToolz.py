def getAgeCategories(dfsArray):
    for extendedDf in dfsArray:
        if  extendedDf['meta']['columns'] == 'AGE' and len(extendedDf['dataFrame'].columns)>4:
            return extendedDf['dataFrame'].columns.tolist()


def getAgeArray(dfsArray):
    allAges = getAgeCategories(dfsArray)
    return [(allAges.index(ageCateg),ageCateg) for ageCateg in allAges]

def getAgeOptions(dfArray,sliderArray):
    options=[]
    agesArray = getAgeArray(dfArray)
    for i in range(sliderArray[0],sliderArray[1]+1):
        options.append(agesArray[i][1])
    return options



def getAllStatesArray(dfsArray):
    states = ["All States"]
    for extendedDf in dfsArray:
        if extendedDf['meta']['state'] not in states:
            states.append(extendedDf['meta']['state'])
    return states

def getDifficultyTypes(dfsArray):
    difficultyTypes = []
    for extendedDf in dfsArray:
        try:
            if extendedDf['meta']['difficulty'] not in difficultyTypes:
                difficultyTypes.append(extendedDf['meta']['difficulty'])
        except:
            pass
    return difficultyTypes


def dfSelector(dfsArray,metaDimension,metaOptions):
    seletedExtendedDfs = []
    for extendedDf in dfsArray:
        for metaOption in metaOptions :
            try:
                if extendedDf['meta'][metaDimension] == metaOption:
                    seletedExtendedDfs.append(extendedDf)
            except:
                pass
    return seletedExtendedDfs


def getRangeCastedNames(ageCategories):
    newArray = []
    for age in ageCategories:
        if age == "Under 5 years" :
            newArray.append("5-")
        elif age =="5 to 17 years":
            newArray.append("17")
        elif age =="18 to 34 years":
            newArray.append("34")
        elif age =="35 to 64 years":
            newArray.append("64")
        elif age =="65 to 74 years":
            newArray.append("74")
        elif age =="75 years and over":
            newArray.append("75+")
    return newArray