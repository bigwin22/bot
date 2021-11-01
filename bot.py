import asyncio
import discord
from datetime import datetime
from discord.client import Client
from discord.ext import commands
import requests
import json
import os

import module.process as process
import module.review as review
from module.mainprocess import Today

#학교코드:7041189

client = commands.Bot(command_prefix='!')  # 명령어 호출 코드
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



#임베드 추가 함수


def printf(title, year, month, day):
    # 임메드 값 추가를 return
    return discord.Embed(title=title, description=year+' '+month+' '+day, color=0x62c1cc)


author = []  # 입력한 유저의 정보 저장

# 급식 명령어


@client.command()
async def 급식(ctx, *val):  # ctx:디스코드 채팅 정보, val:명령의 뒤에 붙는 값들 (ex:이름,년,월,일)
    fpath = "./user/"+str(ctx.author)
    os.makedirs(fpath, exist_ok=T)  # fpath 경로에 폴더가 존재하지 않을 시 생성
    os.makedirs(fpath+'/review', exist_ok=T)

    if (ctx.author in author):  # 같은 사람이 두 개의 이상의 값을 동시에 처리할 경우 무시
        await ctx.channel.send("이미 처리 중이에요")
        return
    author.append(ctx.author)  # 유저 정보 추가

    name = 0  # 학교 이름
    code = 0  # 학교 고유 코드
    ty = 0  # 학교의 유형

    aliases = []  # 같은 이름학교의 2개 이상일 경우의 선택지

    p = await ctx.channel.send("처리 중입니다..............")  # 처리중 메시지 출력

    date = datetime.now()  # 현재 날짜
    print("입력됨", ctx, val)  # 로그 출력
    embed = 0  # 임베드 저장

    store = []  # 음식 값 저장

    try:
        if (len(val) == 0):  # 명령어 뒤에 아무것도 입력되지 않았다면(ex: !급식)
            if (os.path.isfile(fpath+'/code.gf')):  # fpaht에 파일 있다면

                f = open(fpath+"/name.gf", 'r')  # fpath의 name.gf를 읽기모드로 열어라
                x = f.readline()  # 연 파일의 첫 줄을 읽고 변수에 대입
                name = process.setname(x)  # name을 setname(x)의 값으로 구하라
                f.close()  # 파일을 닫아라

                f = open(fpath+"/code.gf", 'r')  # fpath의 code.gf를 읽기모드로 열어라
                x = f.readline()  # 연 파일의 첫 줄을 읽고 변수에 대입
                code = []  # code변수를 빈 list로 만들기
                code.append(x)  # code에 x값을 추가
                f.close()  # 파일을 닫아라

            else:
                await p.delete()  # '처리중입니다'지우기
                await ctx.channel.send("마지막으로 입력된 학교가 없습니다")  # 출력
                del author[author.index(ctx.author)]  # 사용자 정보를 배열에서 지우기.
                return  # 리턴(끝내기)

        elif (len(val) > 0):  # 명령어 뒤에 입력된 값이 있으면
            name = process.setname(val[0])  # name을 setname(val[0])으로 하기
            code = process.getcode(name)  # code를 getcode(name)올 하기

        if (len(code) > 1):  # code안의 값이 2개 이상일 경우
            aliases = []  # 선택지 aliases를 빈 list로 만들기
            add = process.getadd(name)  # add를 getadd(name)의 값으로 하기
            de = 0  # 몇번째로 결정할 것인가

            def check(message):  # wait_for check 함수
                nonlocal de
                # 입력한 값이 aliases안에 message의 내용이 있고/                                                        #message를 입력한 사람와 명령어를 입력한 사람이 같은가
                if ((int(message.content) in aliases) and (message.author == ctx.author)):
                    # de(번호 결정)를 message를 정수로 한거에 -1로 정하기
                    de = int(message.content) - 1
                    return T
                return F

            a = []  # 선택지 출력 저장
            for i in range(len(add)):  # 주소의 갯수만큼 반복
                aliases.append(i+1)  # aliases(선택지)에 i+1를 추가
                # 선택지를 출력하고 이를 a에 추가
                a.append(await ctx.channel.send("```"+str(i+1)+":"+add[i]+"```"))
            b = await ctx.channel.send("(번호)로 입력해주세요 ``예: 1``")  # 출력후 b에 저장

            try:
                # (client.message의 값이 3초안에 check에 부합한가)를 실행후 msg에 저장
                msg = await client.wait_for('message', timeout=3, check=check)
            except asyncio.TimeoutError:  # 시간초과가 날 경우
                for i in range(len(a)):  # a의 값 개수만큼 반복
                    await a[i].delete()  # 출력한 메시지 지우기
                await b.delete()  # 출력한 메시지 지우기
                await p.delete()  # 출력한 메지시 지우기
                await ctx.channel.send(ctx.author.mention+" 선택지 시간 초과")  # 출력
                del author[author.index(ctx.author)]  # 사용자 정보를 배열에서 지우기
                return
            else:
                code = code[de]  # code의 값을 code[de]로 결정(list -> str)
                for i in range(len(a)):  # a에 저장되어 있는 값의 갯수만큼 반복
                    await a[i].delete()  # 출력한 메시지 지우기
                await b.delete()  # 출력한 메시지 지우기
                #await msg.delete()#입력한 메시지 지우기
        else:  # code 값 갯수가 2개 이상이 아닐경우
            code = code[0]  # code는 code[0]으로 하기

        ty = process.gettype(name)  # ty(학교 유형)을 gettype(name)로
        print(code)  # 테스트 코드
        

        when = ['breakfast', 'lunch', 'dinner']  # 아침 점심 저녁

        try:
            today = Today(val)
            embed = printf(name,today.y,today.m,today.d)
            y = today.y  # 년
            m = today.m # 월
            d = today.d  # 일

            for i in range(3):  # 3번 반복
                # store에 getfood값을 추가
                store.append(process.getfood(ty, code, when[i], y, m, d))

            f = open(fpath+"/name.gf", 'w')  # name.gf를 쓰기 모드로 열기
            f.write(name)  # name.gf에 name을 쓰기
            f.close()  # 파일 닫기

            f = open(fpath+"/code.gf", 'w')  # code.gf를 쓰기 모드로 열기
            f.write(code)  # code.gf에 code를 쓰기
            f.close()  # 파일 닫기

        except:
            del author[author.index(ctx.author)]  # 사용자 정보를 배열에서 지우기
            await ctx.channel.send("제대로 입력해주세요")  # 출력
            return
    except:
        del author[author.index(ctx.author)]  # 사용자 정보를 배열에서 지우기
        await ctx.channel.send("학교 이름을 제대로 입력해주세요")  # 출력
        return

    when = ["아침", "점심", "저녁"]  # 아침 점심 저녁
    content = 0  # 내용 여부
    for i in range(3):  # 3번 반복
        if store[i] != '없음':
            content = 1
        # 임베드에 when[i]를 제목으로 store[i]를 내용으로 하여 줄을 내려 출력함을 추가
        embed.add_field(name=when[i], value=store[i], inline=False)
    # 임베드 위에 사용자의 프사와 이름을 추가
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    if (os.path.isdir('./school/'+name)):
        to = open('./school/'+name+'/total.gf', 'r')
        total = to.readline()
        total = float(total.strip('\n'))
        if(os.path.isfile('./school/'+name+'/'+y+m+d+'.gf')):
            t = open('./school/'+name+'/'+y+m+d+'.gf', 'r')
            re = t.readline()
            re = float(re.strip('\n'))
            embed.set_footer(text="이 급식의 평점:"+str(re)+"  학교 전체 평점:"+str(total))
            t.close()
        else:
            embed.set_footer(text="이 급식의 평점:없음  학교 전체 평점:"+str(total))
            to.close()
    else:
        embed.set_footer(text="이 급식의 평점:없음  학교 전체 평점:없음")  # 임베드 마지막에 멘트 추가

    await p.delete()  # 출력된 메시지 지우기
    send = await ctx.channel.send(embed=embed)  # 임베드 값 출력
    ##여기부터 반응 관련 코드
    if (y == str(date.year) and m == str(date.month) and d == str(date.day)) and content == 1 and datetime.today().hour >= 12:
        emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for i in range(5):
            await send.add_reaction(emoji[i])

        def emocheck(reaction):
            if (reaction.user_id == ctx.author.id and reaction.emoji.name in emoji and reaction.message_id == send.id):
                return T  # 리액션을 추가한 유저와 명렁어 유저가 같고 리액션이 리스트에 있으며 리액션 메시지 아이이돠 임베드와 같을 경우

        try:
            reaction = await client.wait_for(event='raw_reaction_add', timeout = 15,check = emocheck)
        except asyncio.TimeoutError:
            await send.delete()
            await ctx.channel.send(embed=embed)
        else:
            review.review(reaction,name,y,m,d,str(ctx.author))
            await send.delete()
            await ctx.channel.send(embed=embed)
            
    del author[author.index(ctx.author)]                                              #사용자 정보를 배열에서 지우기


os.makedirs('./school', exist_ok=T)       
os.makedirs('./user',exist_ok=T)
client.run(token)                                                                     #token 값을 가진 봇을 구동
