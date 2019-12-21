from dfDispatcher import UsaExtractTransform
from pathlib import Path
import os

class UsaExtractTransformMulti:
    def __init__(self,*years):
        for year in years:
            rootPath = str(Path(os.path.realpath(__file__)).parent) + "\\dispatchedRessources\\"
            folderName = year
            if not os.path.isdir(rootPath+folderName):
                os.mkdir(rootPath+folderName)
            folderName = rootPath + year
            dfUs = UsaExtractTransform(year)
            dfUs.dispatcher()

UsaExtractTransformMulti("15","16")

