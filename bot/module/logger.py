from datetime import datetime
from pytz import timezone
import time
import os.path
import os

KST = timezone('Asia/Seoul')
today = str(datetime.now(KST))
today = today.replace(':','#')
os.makedirs('./log',exist_ok=True)
################초기 설정################
if os.path.exists(f'./log/log({today}).log') == False:#실행 날짜의 로그 파일이 없으면
    x = open(f'./log/log({today}).log', 'w')#파일 생성
    x.close()
x = open(f'./log/log({today}).log', 'r')
p = x.readline()
if p == '':#파일 내용에 아무 것도 없으면 날짜선 추가
    x.close()
    x = open(f'./log/log({today}).log', 'a')
    x.write(f'##############{datetime.now(KST)}##############\n')
    x.close()
elif p[16] != datetime.now(KST)[15]:#읽어드리고 현재 날짜와 기록된 날짜가 다르면
    x.close()
    x = open(f'./log/log({today}).log', 'a')
    x.write(f'\n##############{datetime.now(KST)}##############\n')#날자선 추가
    x.close()
###############################################
    

pt = time.time()##처리 시간
def fstarting(name,tag):
    """이 함수는 함수의 시작 시간을 기록합니다."""
    f = open(f'./log/log({today}).log', 'a')
    global pt
    t = datetime.now(KST)
    pt = time.time()
    f.write(f"[{t}]: 함수'{name}'(이)가 시작됨(tag:{tag})\n")
    f.close()
def fend(name,tag):
    """이 함수는 함수의 처리 완료 시간을 기록합니다."""
    f = open(f'./log/log({today}).log', 'a')
    t = datetime.now(KST)
    f.write(f"[{t}]: 함수'{name}'(이)가 끝남/처리 시간:{str(time.time()-pt)}(tag:{tag})\n")
    f.close()



def entered(user,val,tag):
    """이 함수는 언제 어떤 값이 입력되었는지를 기록합니다."""
    f = open(f'./log/log({today}).log','a')
    t = datetime.now(KST)
    f.write(f"[{t}]: {user} entered {val}(tag:{tag})\n")
    f.close()
    

def custom(msg, tag):
    """이 함수는 커스텀 메시지를 기록합니다."""
    f = open(f'./log/log({today}).log','a')
    t = datetime.now(KST)
    f.write(f"[{t}]: {msg}({tag})\n")
    f.close()

