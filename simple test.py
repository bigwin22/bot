import requests
import json

url = "https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&" + "ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7041189&MLSV_YMD=20210915"
response = requests.get(url)
school_infos = json.loads(response.text)

DDISH_NM = [row['DDISH_NM'] for row in school_infos['mealServiceDietInfo'][1]['row']]
on = 1
r = ''
str_add = ''
for c in DDISH_NM[0]:
    if str(c).isdigit():
        continue
    elif c == 'b' or c == 'r':
        continue
    elif c == '>':
        str_add += ','
    elif c == '<' or c == '.' or c == '/':
        continue
    else:
        str_add += c

print(str_add)


