import requests
import json


url = 'https://schoolmenukr.ml/code/api?q=영서중학교'
response = requests.get(url)
school_infos = json.loads(response.text)
school_codes = [info['code'] for info in school_infos['school_infos']]
print(school_infos)




