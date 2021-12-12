import requests
import json
import re



#name의 학교 고유 코드를 구하는 함수(return 값 타입: list)

base = 'KEY=ea324d9b0bfc42c68ade03af97650ce4&TYPE=json'
def basic(name, want,num):
    '''
    학교의 기본 정도를 구하는 코드
    'num'은 여러 학교가 있을 경우: -1(모두)
    '''
    url = 'https://open.neis.go.kr/hub/schoolInfo?'+base+'&SCHUL_NM='+name
    response = requests.get(url)
    infos = json.loads(response.text)
    try:
        val = infos['schoolInfo'][1]['row']
        if (num != -1):
            return val[num][want]
        arr = []
        for i in val:
            arr.append(i[want])
        arr.sort()
        return arr
    except:
        return False

def food(area:str, code:int, when:int, date:str) -> str:
    '''학교 음식을 구해줌, when은 1~3 각각 아침~저녁'''
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo?'\
        +str(base)+'&ATPT_OFCDC_SC_CODE='+area\
        +'&SD_SCHUL_CODE='+str(code)+'&MLSV_YMD='+date\
        +"&MMEAL_SC_CODE=" + str(when)
    response = requests.get(url)
    infos = json.loads(response.text)
    try:
        food = infos["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        food = re.sub(r'[0-9]+','', food)#숫자제거
        food = food.replace('.','')#.제거
        food = food.replace('<br/>',',')#제거
        return food
    except:
        return "없음"

