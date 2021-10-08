import asyncio
import discord
from datetime import datetime
from discord.ext import commands 
import requests
import json
import os

#학교코드:7041189

client = commands.Bot(command_prefix='!')
F = False
T = True

print(datetime.today())

# 생성된 토큰을 입력해준다.
token = "NzczNDQzMjI1NDI3NjQwMzIw.X6JTIg.-RPsiocdBvZslvOvWX0PqXVX5G8"


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
    return code
def getadd(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name
    response = requests.get(url)
    school_infos = json.loads(response.text)
    add = [info['address'] for info in school_infos['school_infos']]
    return add


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


author = []



# 봇이 특정 메세지를 받고 인식하는 코드
@client.command()
async def 급식(ctx, *val):
    name = 0
    code = 0
    ty = 0

    aliases = []

    author.append(ctx.author)

    p = await ctx.channel.send("처리 중입니다..............")

    date = datetime.now()
    print("입력됨", ctx, val)
    embed = 0
    store = []

    fpath = "./user/"+str(ctx.author)

    def pro(a, b, c):
        for i in range(3):
            store.append(getfood(ty, code[0], when[i], a, b, c))

        os.makedirs(fpath, exist_ok=True)

        f = open(fpath+"/name.gf",'w')
        f.write(name)
        f.close()

        f = open(fpath+"/code.gf",'w')
        f.write(code)
        f.close()



    try:
        if (len(val) == 0):
            if (os.path.isdir(fpath)):

                f = open(fpath+"/name.gf", 'r')
                x = f.readline()
                name = setname(x)
                f.close()

                f = open(fpath+"/code.gf", 'r')
                x = f.readline()
                code = []
                code.append(x)
                f.close()

            else:
                await p.delete()
                await ctx.channel.send("마지막으로 입력된 학교가 없습니다")
                return

        elif (len(val) > 0):
            name = setname(val[0])
            code = getcode(name)

        if (len(code) > 1):
            aliases = []
            add = getadd(name)
            de = 0 #몇번째로 결정할 것인가 

            def check(message):
                global de

                if ((int(message.content) in aliases) and (
                        message.author == ctx.author)):
                    de = int(message.content) - 1
                    return T
                return F

            a = []
            for i in range(len(add)):
                aliases.append(i+1)
                a.append(await ctx.channel.send("```"+str(i+1)+":"+add[i]+"```"))
            b = await ctx.channel.send("(번호)로 입력해주세요 ``예: 1``")

            try:
                msg = await client.wait_for('message',timeout=3,check=check)
            except asyncio.TimeoutError:
                for i in range(len(a)):
                    await a[i].delete()
                await b.delete()
                await p.delete()
                await ctx.channel.send(ctx.author.mention+" 선택지 시간 초과")
                return
            else:
                code = code[de]
                for i in range(len(a)):
                    await a[i].delete()
                await b.delete( )
                await msg.delete()
        else:
            code = code[0]

        ty = gettype(name)

        when = ['breakfast','lunch','dinner']

        try:
            if (len(val) == 4):
                pro(val[1],val[2],val[3])
                embed = printf(name,val[1],val[2],val[3])
            elif (len(val) == 3):
                pro(str(date.year),val[1],val[2])
                embed = printf(name,str(date.year),val[1],val[2])
            elif (len(val) == 1 or len(val) == 0):
                pro(str(date.year),str(date.month),str(date.day))
                embed = printf(name,str(date.year),str(date.month),str(date.day))

        except:
            await ctx.channel.send("제대로 입력해주세요")
    except:
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")

    when = ["아침", "점심", "저녁"]
    for i in range(3):
        embed.add_field(name=when[i],value=store[i],inline=False)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)    
    embed.set_footer(text="이상입니다") 

    await p.delete()

    await ctx.channel.send(embed=embed)


client.run(token)