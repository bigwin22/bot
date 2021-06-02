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


def four(n):
    if (len(str(n)) == 4):
        return 4
    return 0


def getcode(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name
    response = requests.get(url)
    school_infos = json.loads(response.text)
    code = [info['code'] for info in school_infos['school_infos']]
    val = ''
    for a in code:
        val += a
    return val

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

    name = ''
    code = ''
    type = ''

    breakfast = 2
    lunch = 3
    dinner = 4

    embed = 0

    try:
        name = setname(val[0])
        code = getcode(name)
        ty = gettype(name)
        try:
            if (len(val) == 4):
                breakfast = getfood(ty, code, 'breakfast', val[1], val[2], val[3])
                lunch = getfood(ty, code, 'lunch', val[1], val[2], val[3])
                dinner = getfood(ty, code, 'dinner', val[1], val[2], val[3])
                embed = printf(val[0],val[1],val[2],val[3])
            elif (len(val) == 3):
                breakfast = getfood(ty, code, 'breakfast', str(date.year), val[1], val[2])
                lunch = getfood(ty, code, 'lunch', str(date.year), val[1], val[2])
                dinner = getfood(ty, code, 'dinner', str(date.year), val[1], val[2])
                embed = printf(val[0],str(date.year),val[1],val[2])
            if (len(val) == 1):
                breakfast = getfood(ty, code, 'breakfast', str(date.year), str(date.month), str(date.day))
                lunch = getfood(ty, code, 'lunch', str(date.year), str(date.month), str(date.day))
                dinner = getfood(ty, code, 'dinner', str(date.year), str(date.month), str(date.day))
                embed = printf(val[0],str(date.year),str(date.month),str(date.day))
        except:
            await ctx.channel.send("제대로 입력해주세요")
    except:
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")

    embed.add_field(name="아침", value=breakfast,inline=False)
    embed.add_field(name="점심", value=lunch,inline=False)
    embed.add_field(name="저녁", value=dinner,inline=False)
    embed.set_footer(text="이상입니다")
    await ctx.channel.send(embed=embed)


'''async def 타이머(ctx, *text):'''

client.run(token)