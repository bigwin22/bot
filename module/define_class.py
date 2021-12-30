from datetime import datetime

import School as school
date = datetime.now()

class Today():
    def __init__(self,val):
        date = datetime.now()
        if len(val) == 4:
            self.y=val[1]
            self.m=val[2]
            self.d=val[3]
        elif len(val) == 3:
            self.y = str(date.year)
            self.m = val[1]
            self.d = val[2]
        elif len(val) == 1 or len(val) == 0:
            self.y = str(date.year)
            self.m = str(date.month)
            self.d = str(date.day)
class School():
    def school(self, name,num):
        self.name = school.basic(name, 'SCHUL_NM',num)
        self.add = school.basic(name, 'ORG_RDNMA', num)
        self.area = school.basic(name, 'ATPT_OFCDC_SC_CODE',num)
        self.code = school.basic(name, 'SD_SCHUL_CODE', num)
    def setting(self,num):
        self.name = self.name[num]
        self.add = self.add[num]
        self.area = self.area[num]
        self.code = self.code[num]

        
