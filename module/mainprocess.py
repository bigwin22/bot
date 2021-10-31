from datetime import datetime
date = datetime.today()

class Today():
    def __init__(self,val):
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
