import asyncio
import discord
from datetime import datetime
from discord.client import Client
from discord.ext import commands 
import requests
import json
import os

#학교코드:7041189

client = commands.Bot(command_prefix='!')                                               #명령어 호출 코드
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

#name의 학교 고유 코드를 구하는 함수(return 값 타입: list)
def getcode(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name                                   #api의 url 저장
    response = requests.get(url)
    school_infos = json.loads(response.text)                                             #json을 파싱
    code = [info['code'] for info in school_infos['school_infos']]                       #school_infos의 code값 추출
    return code

#name의 학교의 주소를 구하는 함수(return 값 타입: list)
def getadd(name):
    url = "https://schoolmenukr.ml/code/api?q=" + name                                  #api의 url 저장
    response = requests.get(url)
    school_infos = json.loads(response.text)                                            #json을 파싱
    add = [info['address'] for info in school_infos['school_infos']]                    #school_infos의 address값 추출
    return add

#name을 완전한 이름으로 변환(ex: 영서중 -> 영서중학교)
def setname(name):
    em = list(name)                                                                     #str을 list 변환
    em.reverse()                                                                        #이름 뒤집기
    app = ''
    if (em[0]=='초' or em[0] == '고'):                                                  #뒤집고 나서 앞에 있는 글자로 완전 여부 파악후 이름 완성
        app = '등학교'
    elif(em[0]=='중'):
        app = '학교'
    em.reverse()
    if (app == ''):
        return name
    return name+app

#name의 학교의 타입을 구하는 함수(ex: 한국디지털미디어고등학교 -> high/영서중 -> middle)
def gettype(name):
    em = list(name)                                                                    #str을 list로 변환
    em.reverse()                                                                       #이름 뒤집기
    if (em[2] == '중'):                                                                #뒤집고 나서 앞에 있는 글자로 학교의 유형 파악
        return "middle"
    elif (em[2] == '등'):
        if (em[3] == '초'):
            return "elementary"
        else:
            return "high"

#급식 리스트를 구하는 함수(ty:학교의 유형(elementary,middle,high), code:학교 고유 코드,when:(아침,점심,저녁)
#                         year,month,day:년,월,일) 
def getfood(ty,code,when, year,month,day):
    url ='https://schoolmenukr.ml/api/'+ty+'/'+code+'?'+'year='+year+'&'+'month='+month+'&'+'date='+day+'&'+'allergy='+'hidden'#api 링크
    response = requests.get(url)
    school_infos = json.loads(response.text)                                          #json 파싱
    code = [info[when] for info in school_infos['menu']]                              #menu의 'when'의 값 추출
    p = ''
    for a in code:#음식이름에 ',' 추가
        for x in a:
            p += x + ', '
    if (p == ''):
        return "없음"
    return p

#임베드 추가 함수
def printf(title, year, month, day):
    return discord.Embed(title=title,description=year+' '+month+' '+day,color=0x62c1cc)#임메드 값 추가를 return


author = []                                                                           #입력한 유저의 정보 저장

# 급식 명령어
@client.command()
async def 급식(ctx, *val):                                                            #ctx:디스코드 채팅 정보, val:명령의 뒤에 붙는 값들 (ex:이름,년,월,일)

    if (ctx.author in author):                                                        #같은 사람이 두 개의 이상의 값을 동시에 처리할 경우 무시
        await ctx.channel.send("이미 처리 중이에요")
        return
    author.append(ctx.author)                                                         #유저 정보 추가

    name = 0                                                                          #학교 이름
    code = 0                                                                          #학교 고유 코드
    ty = 0                                                                            #학교의 유형

    aliases = []                                                                      #같은 이름학교의 2개 이상일 경우의 선택지

    p = await ctx.channel.send("처리 중입니다..............")                          #처리중 메시지 출력

    date = datetime.now()                                                             #현재 날짜
    print("입력됨", ctx, val)                                                         #로그 출력
    embed = 0                                                                         #임베드 저장

    store = []                                                                        #음식 값 저장

    fpath = "./user/"+str(ctx.author)                                                 #정보 저장 경로

    try:
        if (len(val) == 0):                                                           #명령어 뒤에 아무것도 입력되지 않았다면(ex: !급식)
            if (os.path.isdir(fpath)):                                                #fpaht경로가 있다면

                f = open(fpath+"/name.gf", 'r')                                       #fpath의 name.gf를 읽기모드로 열어라
                x = f.readline()                                                      #연 파일의 첫 줄을 읽고 변수에 대입
                name = setname(x)                                                     #name을 setname(x)의 값으로 구하라
                f.close()                                                             #파일을 닫아라

                f = open(fpath+"/code.gf", 'r')                                       #fpath의 code.gf를 읽기모드로 열어라
                x = f.readline()                                                      #연 파일의 첫 줄을 읽고 변수에 대입
                code = []                                                             #code변수를 빈 list로 만들기
                code.append(x)                                                        #code에 x값을 추가
                f.close()                                                             #파일을 닫아라

            else:
                await p.delete()                                                      #'처리중입니다'지우기
                await ctx.channel.send("마지막으로 입력된 학교가 없습니다")             #출력
                del author[author.index(ctx.author)]                                  #사용자 정보를 배열에서 지우기.
                return#리턴(끝내기)

        elif (len(val) > 0):                                                          #명령어 뒤에 입력된 값이 있으면
            name = setname(val[0])                                                    #name을 setname(val[0])으로 하기
            code = getcode(name)                                                      #code를 getcode(name)올 하기
            

        if (len(code) > 1):                                                           #code안의 값이 2개 이상일 경우
            aliases = []                                                              #선택지 aliases를 빈 list로 만들기
            add = getadd(name)                                                        #add를 getadd(name)의 값으로 하기
            de = 0                                                                    #몇번째로 결정할 것인가 

            def check(message):                                                       #wait_for check 함수
                nonlocal de
                if ((int(message.content) in aliases) and (message.author == ctx.author)):#입력한 값이 aliases안에 message의 내용이 있고/                                                        #message를 입력한 사람와 명령어를 입력한 사람이 같은가
                    de = int(message.content) - 1                                     #de(번호 결정)를 message를 정수로 한거에 -1로 정하기
                    return T
                return F

            a = []                                                                    #선택지 출력 저장
            for i in range(len(add)):                                                 #주소의 갯수만큼 반복  
                aliases.append(i+1)                                                   #aliases(선택지)에 i+1를 추가
                a.append(await ctx.channel.send("```"+str(i+1)+":"+add[i]+"```"))     #선택지를 출력하고 이를 a에 추가
            b = await ctx.channel.send("(번호)로 입력해주세요 ``예: 1``")              #출력후 b에 저장

            try:
                msg = await client.wait_for('message',timeout=3,check=check)          #(client.message의 값이 3초안에 check에 부합한가)를 실행후 msg에 저장
            except asyncio.TimeoutError:                                              #시간초과가 날 경우
                for i in range(len(a)):                                               #a의 값 개수만큼 반복
                    await a[i].delete()                                               #출력한 메시지 지우기
                await b.delete()                                                      #출력한 메시지 지우기
                await p.delete()                                                      #출력한 메지시 지우기
                await ctx.channel.send(ctx.author.mention+" 선택지 시간 초과")         #출력
                del author[author.index(ctx.author)]                                  #사용자 정보를 배열에서 지우기
                return
            else:
                code = code[de]                                                       #code의 값을 code[de]로 결정(list -> str)
                for i in range(len(a)):                                               #a에 저장되어 있는 값의 갯수만큼 반복
                    await a[i].delete()                                               #출력한 메시지 지우기
                await b.delete( )                                                     #출력한 메시지 지우기
                #await msg.delete()#입력한 메시지 지우기
        else:                                                                         #code 값 갯수가 2개 이상이 아닐경우
            code = code[0]                                                            #code는 code[0]으로 하기

        ty = gettype(name)                                                            #ty(학교 유형)을 gettype(name)로
        print(code)## #테스트 코드

        when = ['breakfast','lunch','dinner']                                         #아침 점심 저녁

        try:
            y = 0                                                                     #년
            m = 0                                                                     #월
            d = 0                                                                     #일
            if (len(val) == 4):                                                       #명령어 뒤에 입력된게 4개일 경우
                #val[0]:학교 이름
                y = val[1]                                                            #val[1]:(이름 뒤에 year)
                m = val[2]                                                            #val[2]:month
                d = val[3]                                                            #val[3]:day
                embed = printf(name,val[1],val[2],val[3])                             #임베드를 printf값으로 결정
            elif (len(val) == 3):
                y = str(date.year)                                                    #현재 년도
                m = val[1]                                                            #val[1]:(이름 뒤에 year)
                d = val[2]                                                            #val[2]:month
                embed = printf(name,str(date.year),val[1],val[2])                     #임베드를 printf값으로 결정
            elif (len(val) == 1 or len(val) == 0):
                y = str(date.year)                                                    #현재 년도로
                m = str(date.month)                                                   #현재 월로
                d = str(date.day)                                                     #현재 일로
                embed = printf(name,str(date.year),str(date.month),str(date.day))     #임베드를 printf값으로 결정

            for i in range(3):                                                        #3번 반복
                store.append(getfood(ty, code, when[i], y, m, d))                     #store에 getfood값을 추가

            os.makedirs(fpath, exist_ok=True)                                         #fpath 경로에 폴더가 존재하지 않을 시 생성

            f = open(fpath+"/name.gf",'w')                                            #name.gf를 쓰기 모드로 열기
            f.write(name)                                                             #name.gf에 name을 쓰기
            f.close()                                                                 #파일 닫기

            f = open(fpath+"/code.gf",'w')                                            #code.gf를 쓰기 모드로 열기
            f.write(code)                                                             #code.gf에 code를 쓰기
            f.close()                                                                 #파일 닫기

        except:
            del author[author.index(ctx.author)]                                      #사용자 정보를 배열에서 지우기
            await ctx.channel.send("제대로 입력해주세요")                              #출력
            return
    except:
        del author[author.index(ctx.author)]                                          #사용자 정보를 배열에서 지우기
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")                       #출력
        return

    when = ["아침", "점심", "저녁"]#아침 점심 저녁
    for i in range(3):#3번 반복
        embed.add_field(name=when[i],value=store[i],inline=False)                     #임베드에 when[i]를 제목으로 store[i]를 내용으로 하여 줄을 내려 출력함을 추가
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)             #임베드 위에 사용자의 프사와 이름을 추가
    embed.set_footer(text="이상입니다")                                                #임베드 마지막에 멘트 추가

    await p.delete()                                                                  #출력된 메시지 지우기

    emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
    send =await ctx.channel.send(embed=embed)                                         #임베드 값 출력
    for i in range(5):
        await send.add_reaction(emoji[i])


    def emocheck(reaction):  
        if (reaction.user_id == ctx.author.id and reaction.emoji.name in emoji and reaction.message_id == send.id):
            return T                                                                  #리액션을 추가한 유저와 명렁어 유저가 같고 리액션이 리스트에 있으며 리액션 메시지 아이이돠 임베드와 같을 경우

    try:
        reaction = await client.wait_for(event='raw_reaction_add', timeout = 15,check = emocheck)
    except asyncio.TimeoutError:
        await ctx.channel.send("시간초과")
    else:
        fpath = "./school/"
        os.makedirs(fpath, exist_ok=True)

        f = open(fpath+"/"+name+'.gf','rw')
        

        
        
    await send.delete()
    await ctx.channel.send(embed=embed)
 

    del author[author.index(ctx.author)]                                              #사용자 정보를 배열에서 지우기


client.run(token)                                                                     #token 값을 가진 봇을 구동