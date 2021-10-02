import asyncio
import discord
from discord.ext import commands
import requests
import json
import os

##학교코드:7041189

client = commands.Bot(command_prefix='!')
F = False
T = True

# 생성된 토큰을 입력해준다.
token = "NzczNDQzMjI1NDI3NjQwMzIw.X6JTIg.Ebjq6ThJUXCck6kSaIEhMQd9VW8"

# 봇이 구동되었을 때 보여지는 코드
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")

<<<<<<< HEAD

=======
>>>>>>> parent of e7b8091 (디코봇)
def getcode(name):
    url = 'https://schoolmenukr.ml/code/api?q=' + name
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




work = []
aliases = []

author = []

name = []
code = []
ty = []


##
@client.command()
async def test(ctx, val):
    arr = [work,aliases,name,code,ty,author,author.index(ctx.author)]
    await ctx.channel.send(arr[int(val)-1][author.index(ctx.author)])
    await ctx.channel.send(type(arr[int(val)-1][author.index(ctx.author)]))

@client.command(aliases = [''])
async def pick(ctx, val):
    global work, choice, aliases
    global code
    if ((int(val) in aliases[author.index(ctx.author)]) and work[author.index(ctx.author)] == T and (ctx.author==author[author.index(ctx.author)])):
        await ctx.channel.purge(limit=len(code[author.index(ctx.author)])+2)
        work[author.index(ctx.author)] = F
        aliases[author.index(ctx.author)] = []
        code[author.index(ctx.author)] = code[author.index(ctx.author)][int(val)-1]




# 봇이 특정 메세지를 받고 인식하는 코드
@client.command()
async def 급식(ctx, *val):
<<<<<<< HEAD
    global work, choice ,aliases, author
    global name, code, ty

    name.append(None), code.append(None), ty.append(None), work.append(None),aliases.append(None)
    author.append(ctx.author)

    await ctx.channel.send("처리 중입니다..............")

    date = datetime.now()
    print("입력됨", ctx, val)
    embed = 0
    store = []

    def pro(a, b, c):
        for i in range(3):
            store.append(getfood(ty[author.index(ctx.author)], code[author.index(ctx.author)], when[i], a, b, c))
        f = open(str(ctx.author) + ".gf",'w')
        f.write(name[author.index(ctx.author)])
        f.close()

    try:
        if (len(val) == 0):
            print(1)
            if (os.path.isfile(str(ctx.author) + ".gf")):
                print(1)

                f = open(str(ctx.author) + ".gf", 'r')
                x = f.readline()
                name[author.index(ctx.author)] = setname(x)
            else:
                print(2)
                await ctx.channel.send("마지막으로 입력된 학교가 없습니다")
                return

        elif (len(val) > 0):
            name[author.index(ctx.author)] = setname(val[0])
        code[author.index(ctx.author)] = getcode(name[author.index(ctx.author)])
        print(code[author.index(ctx.author)], len(code[author.index(ctx.author)]))##
        if (len(code[author.index(ctx.author)]) > 1):
            aliases[author.index(ctx.author)] = []
            add = getadd(name[author.index(ctx.author)])
            work[author.index(ctx.author)] = T

            for i in range(len(add)):
                aliases[author.index(ctx.author)].append(i+1)
                await ctx.channel.send("```"+str(i+1)+":"+add[i]+"```")
            await ctx.channel.send("(!+번호)로 입력해주세요 ``예: ! 1``")
            await asyncio.sleep(5)
        else:
            code[author.index(ctx.author)] = code[author.index(ctx.author)][0]

        ty[author.index(ctx.author)] = gettype(name[author.index(ctx.author)])

        when = ['breakfast','lunch','dinner']

        try:
            if (len(val) == 4):
                pro(val[1],val[2],val[3])
                embed = printf(name[author.index(ctx.author)],val[1],val[2],val[3])
            elif (len(val) == 3):
                pro(str(date.year),val[1],val[2])
                embed = printf(name[author.index(ctx.author)],str(date.year),val[1],val[2])
            elif (len(val) == 1 or len(val) == 0):
                pro(str(date.year),str(date.month),str(date.day))
                embed = printf(name[author.index(ctx.author)],str(date.year),str(date.month),str(date.day))
        except:
            await ctx.channel.send("제대로 입력해주세요")
    except:
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")

    when = ["아침", "점심", "저녁"]
    for i in range(3):
        embed.add_field(name=when[i],value=store[i],inline=False)
    embed.set_footer(text="이상입니다")

    await ctx.channel.purge(limit=1)
    await ctx.channel.send(embed=embed)
=======
    code = getcode(val[0])
    typ = gettype(val[0])
    #food = getfood(val,code,typ)
    await ctx.send(code+' '+typ)
>>>>>>> parent of e7b8091 (디코봇)

    del work[author.index(ctx.author)],aliases[author.index(ctx.author)], name[author.index(ctx.author)],code[author.index(ctx.author)],ty[author.index(ctx.author)]
    del author[author.index(ctx.author)]




client.run(token)