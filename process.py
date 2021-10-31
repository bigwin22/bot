import requests
import json



#name의 학교 고유 코드를 구하는 함수(return 값 타입: list)


def getcode(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name  # api의 url 저장
    response = requests.get(url)
    school_infos = json.loads(response.text)  # json을 파싱
    code = [info['code']
        for info in school_infos['school_infos']]  # school_infos의 code값 추출
    return code

#name의 학교의 주소를 구하는 함수(return 값 타입: list)


def getadd(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name  # api의 url 저장
    response = requests.get(url)
    school_infos = json.loads(response.text)  # json을 파싱
    add = [info['address']
        for info in school_infos['school_infos']]  # school_infos의 address값 추출
    return add

#name을 완전한 이름으로 변환(ex: 영서중 -> 영서중학교)


def setname(name):
    em = list(name)  # str을 list 변환
    em.reverse()  # 이름 뒤집기
    app = ''
    if (em[0] == '초' or em[0] == '고'):  # 뒤집고 나서 앞에 있는 글자로 완전 여부 파악후 이름 완성
        app = '등학교'
    elif(em[0] == '중'):
        app = '학교'
    em.reverse()
    if (app == ''):
        return name
    return name+app

#name의 학교의 타입을 구하는 함수(ex: 한국디지털미디어고등학교 -> high/영서중 -> middle)


def gettype(name):
    em = list(name)  # str을 list로 변환
    em.reverse()  # 이름 뒤집기
    if (em[2] == '중'):  # 뒤집고 나서 앞에 있는 글자로 학교의 유형 파악
        return "middle"
    elif (em[2] == '등'):
        if (em[3] == '초'):
            return "elementary"
        else:
            return "high"

#급식 리스트를 구하는 함수(ty:학교의 유형(elementary,middle,high), code:학교 고유 코드,when:(아침,점심,저녁)
#                         year,month,day:년,월,일)


def getfood(ty, code, when, year, month, day):
    url = 'https://schoolmenukr.ml/api/'+ty+'/'+code+'?'+'year='+year + \
        '&'+'month='+month+'&'+'date='+day+'&'+'allergy='+'hidden'  # api 링크
    response = requests.get(url)
    school_infos = json.loads(response.text)  # json 파싱
    code = [info[when] for info in school_infos['menu']]  # menu의 'when'의 값 추출
    p = ''
    for a in code:  # 음식이름에 ',' 추가
        for x in a:
            p += x + ', '
    if (p == ''):
        return "없음"
    return p