from ageSexeHCP04 import loader1
from matrimonialSexeHCP04 import loader2
from illiteracySexeEnvirHCP04 import loader3
from illiteracySexeAgeHCP04 import loader4

class EtlHcp04:
    extendedDataFrames = []
    def __init__(self):
        self.extendedDataFrames.append(loader1.main())
        self.extendedDataFrames.append(loader2.main())
        self.extendedDataFrames.append(loader3.main())
        self.extendedDataFrames.append(loader4.main())

if __name__ == "__main__":
    res = EtlHcp04()
    for r in res.extendedDataFrames:
        for rr in r:
            print(rr)