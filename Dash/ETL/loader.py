from ETL.ETL_HCP04.ageSexeHCP04 import loader1
from ETL.ETL_HCP04.matrimonialSexeHCP04 import loader2
from ETL.ETL_HCP04.illiteracySexeEnvirHCP04 import loader3
from ETL.ETL_HCP04.illiteracySexeAgeHCP04 import loader4
from ETL.ETL_HCP04.educationEnvirHCP04 import loader5
from ETL.ETL_HCP04.activityEnvirHCP04 import loader6

class EtlHcp04:
    extendedDataFrames = []
    def __init__(self):
        self.extendedDataFrames.append(loader1.main())
        self.extendedDataFrames.append(loader2.main())
        self.extendedDataFrames.append(loader3.main())
        self.extendedDataFrames.append(loader4.main())
        self.extendedDataFrames.append(loader5.main())
        self.extendedDataFrames.append(loader6.main())

if __name__ == "__main__":
    res = EtlHcp04()
    for r in res.extendedDataFrames:
        for rr in r:
            print(rr)