from datetime import datetime
from pytz import timezone
import time
import os.path

KST = timezone('Asia/Seoul')

start = datetime.now(KST)
today = str(datetime.now(KST))
today = today.replace(':','#')
print(datetime.now(KST))
################Initial setting################
if os.path.exists(f'./log/log({today}).log') == False:
    x = open(f'./log/log({today}).log', 'w')
    x.close()
x = open(f'./log/log({today}).log', 'r')
p = x.readline()
if p == '':
    x.close()
    x = open(f'./log/log({today}).log', 'a')
    x.write(f'##############{datetime.now(KST)}##############\n')
    x.close()
elif p[16] != datetime.now(KST)[15]:
    x.close()
    x = open(f'./log/log({today}).log', 'a')
    x.write(f'\n##############{datetime.now(KST)}##############\n')
    x.close()
###############################################
    

pt = time.time()##processing time
def fstarting(name,tag):
    """This Function records when the'Function' stared"""
    f = open(f'./log/log({today}).log', 'a')
    global pt
    t = datetime.now(KST)
    pt = time.time()
    f.write(f"[{t}]: Function'{name}' has begun(tag:{tag})\n")
    f.close()
def fend(name,tag):
    """This Function records when the'Function' started"""
    f = open(f'./log/log({today}).log', 'a')
    t = datetime.now(KST)
    f.write(f"[{t}]: Function'{name}' is done/Processing time:{str(time.time()-pt)}(tag:{tag})\n")
    f.close()



def entered(user,val,tag):
    """This Function records when it was entered"""
    f = open(f'./log/log({today}).log','a')
    t = datetime.now(KST)
    f.write(f"[{t}]: {user} entered {val}(tag:{tag})\n")
    f.close()
    

def custom(msg, tag):
    """This Function records custom log message"""
    f = open(f'./log/log({today}).log','a')
    t = datetime.now(KST)
    f.write(f"[{t}]: {msg}({tag})\n")
    f.close()

