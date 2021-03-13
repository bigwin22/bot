import asyncio
import discord
from discord.ext import commands
import requests
import json

##학교코드:7041189

client = commands.Bot(command_prefix='!')

# 생성된 토큰을 입력해준다.
token = "NzczNDQzMjI1NDI3NjQwMzIw.X6JTIg.Ebjq6ThJUXCck6kSaIEhMQd9VW8"

# 봇이 구동되었을 때 보여지는 코드
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")

def getcode(name):
    url = 'https://schoolmenukr.ml/code/api?q=' + name
    response = requests.get(url)
    school_infos = json.loads(response.text)
    code = [info['code'] for info in school_infos['school_infos']]
    val = ''
    for a in code:
        val += a
    return val

def gettype(name):
    url = 'https://schoolmenukr.ml/code/api?q=' + name
    response = requests.get(url)
    school_infos = json.loads(response.text)
    code = [info['estType'] for info in school_infos['school_infos']]
    val = ''
    for a in code:
        val += a
    return val

def getfood(*arr, code, type):
    url = 'https://schoolmenukr.ml/api/'+type+'/'+code+'?'
    response = requests.get(url)
    school_menu = json.loads(response.text)
    test = [info['lunch'] for info in school_infos['menu']]
    val = ''
    for a in test:
        val += a
    print(val)



# 봇이 특정 메세지를 받고 인식하는 코드
@client.command()
async def 급식(ctx, *val):
    code = getcode(val[0])
    typ = gettype(val[0])
    #food = getfood(val,code,typ)
    await ctx.send(code+' '+typ)


'''async def 타이머(ctx, *text):'''


client.run(token)