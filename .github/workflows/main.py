import asyncio
import discord
from datetime import datetime
from discord.ext import commands
import requests
import json

##학교코드:7041189

client = commands.Bot(command_prefix='!')

print(datetime.today())

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
    url = "https://schoolmenukr.ml/code/api?q=" + name
    response = requests.get(url)
    school_infos = json.loads(response.text)
    code = [info['code'] for info in school_infos['school_infos']]
    return code[0]


def setname(name):
    em = list(name)
    em.reverse()
    app = ''
    if (em[0]=='초' or em[0] == '고'):
        app = '등학교'
    elif(em[0]=='중'):
        app = '학교'
    em.reverse()
    if (app == ''):
        return name
    return name+app

def gettype(name):
    em = list(name)
    em.reverse()
    if (em[2] == '중'):
        return "middle"
    elif (em[2] == '등'):
        if (em[3] == '초'):
            return "elementary"
        else:
            return "high"

def getfood(ty,code,when, year,month,day):
    url ='https://schoolmenukr.ml/api/'+ty+'/'+code+'?'+'year='+year+'&'+'month='+month+'&'+'date='+day+'&'+'allergy='+'hidden'
    response = requests.get(url)
    school_infos = json.loads(response.text)
    code = [info[when] for info in school_infos['menu']]
    p = ''
    for a in code:
        for x in a:
            p += x + ', '
    if (p == ''):
        return "없음"
    return p

def printf(title, year, month, day):
    return discord.Embed(title=title,description=year+' '+month+' '+day,color=0x62c1cc)

# 봇이 특정 메세지를 받고 인식하는 코드
@client.command()
async def 급식(ctx, *val):
    date = datetime.now()
    print("입력됨", ctx, val)
    embed = 0
    store = []
    try:
        name = setname(val[0])
        code = getcode(name)
        ty = gettype(name)

        when = ['breakfast','lunch','dinner']

        try:
            if (len(val) == 4):
                for i in range(3):
                    store.append(getfood(ty, code, when[i], val[1], val[2], val[3]))
                embed = printf(name,val[1],val[2],val[3])
            elif (len(val) == 3):
                for i in range(3):
                    store.append(getfood(ty, code, when[i], str(date.year), val[1], val[2]))
                embed = printf(name,str(date.year),val[1],val[2])
            if (len(val) == 1):
                for i in range(3):
                    store.append(getfood(ty, code, when[i], str(date.year), str(date.month), str(date.day)))
                embed = printf(name,str(date.year),str(date.month),str(date.day))
        except:
            await ctx.channel.send("제대로 입력해주세요")
    except:
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")

    when = ["아침", "점심", "저녁"]
    for i in range(3):
        embed.add_field(name=when[i],value=store[i],inline=False)
    embed.set_footer(text="이상입니다")
    await ctx.channel.send(embed=embed)


client.run(token)