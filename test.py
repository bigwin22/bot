import requests
import json


url = 'https://schoolmenukr.ml/code/api?q=영서중학교'
response = requests.get(url)
school_infos = json.loads(response.text)
print(school_infos)

url = 'https://schoolmenukr.ml/api/middle/B100001189?year=2019&month=10&date=21&allergy=hidden'
response = requests.get(url)
school_menu = json.loads(response.text)
print(school_menu)