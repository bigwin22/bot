import asyncio
import discord
from datetime import datetime
from discord.client import Client
from discord.ext import commands
import requests
import json
import os

# 내가 만든 module
import module.process as process  # moduel 폴더의 process 모듈을 process로 규정하여 import해라
import module.review as review  # 이하동문
# import 'Today' funtion in mainprocess in module folder
from module.mainprocess import Today
from module.mainprocess import School

# 학교코드:7041189

client = commands.Bot(command_prefix='!')  # 명령어 호출 코드
F = False
T = True

print(datetime.today())

# 생성된 토큰을 입력해준다.
token = open('token.token', 'r')
token = str(token.readline())

# 봇이 구동되었을 때 보여지는 코드


@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")


# 임베드 추가 함수


def printf(title, year, month, day):
    # 임메드 값 추가를 return
    return discord.Embed(title=title, description=year+' '+month+' '+day, color=0x62c1cc)


author = []  # 입력한 유저의 정보 저장

# 급식 명령어


@client.command()
async def 급식(ctx, *val):  # ctx:디스코드 채팅 정보, val:명령의 뒤에 붙는 값들 (ex:이름,년,월,일)
    date = datetime.now()
##################################################처리 시작 코드#######################
    fpath = "./user/"+str(ctx.author)
    os.makedirs(fpath, exist_ok=T)  # fpath 경로에 폴더가 존재하지 않을 시 생성
    os.makedirs(fpath+'/review', exist_ok=T)

    if (ctx.author in author):  # 같은 사람이 두 개의 이상의 값을 동시에 처리할 경우 무시
        await ctx.channel.send("이미 처리 중이에요")
        return
    author.append(ctx.author)  # 유저 정보 추가

    p = await ctx.channel.send("처리 중입니다..........")
#######################################################################################

###################################################기본 세팅(변수,함수)##########################
    school = School()

    choice = 0 #선택지
    clist = [] #choice list 선택지
    cprint = [] #choice 출력 배열
    def check(message) -> bool: #선택지 함수
        """선택지의 T,F 여부"""
        nonlocal choice
        if int(message.content) in clist and message.author == ctx.author:
            choice = int(message.content) - 1
            return T
        return F
    
    store = []
 ##################################################################################### 

#######################################경우에 수에 따른 변수 값 지정#####################
    if len(val) == 0:
        if os.path.isfile(fpath+'/name.gf', 'r'):
            f = open(fpath+'/name.gf', 'r')
            em = f.readline()
            school.name = em
            f.close()

            f = open(fpath+'/code.gf', 'r')
            em = f.readline()
            school.area = em[0:3]
            school.code = em[3:]
            f.close()
        else:
            await p.delete()
            await ctx.channel.send("마지막으로 입력된 학교가 없습니다.")
            del author[author.index(ctx.author)]
            return
    elif len(val) > 0:
        if os.path.isfile('./user/'+str(ctx.author)+'/shorts/'+val[0]+'.gf'):
            f = open('./user/'+str(ctx.author)+'/shorts/'+val[0]+'.gf','r')
            school.school(str(f.readline()),-1)
        else:
            school.school(val[0],-1)
        if len(school.name) > 1:
            clist = []
            cprint = []
            for i in range(len(school.name)):
                clist.append(i+1)
                cprint.append(await ctx.channel.send("```"+str(i+1)+":"+school.name[i]+'('+school.add[i]+')'+"```"))
            a = await ctx.channel.send("(번호)로 입력해주세요 ``예: 1``")

            try:
                msg = await client.wait_for('message', timeout=len(school.name)+6, check=check)
            except asyncio.TimeoutError:
                for i in range(len(cprint)):
                    await cprint[i].delete()
                await a.delete()
                await p.delete()
                await ctx.channel.send(ctx.author.mention+" 선택지 시간 초과")
                del author[author.index(ctx.author)]
                return
            else:
                school.setting(choice)
                for i in range(len(cprint)):
                    await cprint[i].delete()
                await a.delete()
        else:
            school.setting(0)               
###################################################################################################

##############################################급식 정보###########################################
    today = Today(val)
    embed = printf(school.name, today.y,today.m,today.d)
    y = today.y
    m = today.m
    d = today.d

    for i in range(3):
        store.append(process.food(school.area,school.code,i+1,y+m+d))
    f = open(fpath+"/name.gf", 'w')
    f.write(school.name)
    f.close()

    f = open(fpath+"/code.gf",'w')
    f.write(school.code)
    f.close()
##################################################################################################

######################################급식 정보 출력##################################################
    when = ['아침','점심','저녁']
    content = 0
    for i in range(3):
        if store[i] != '없음':
            content = 1
        embed.add_field(name=when[i],value=store[i],inline=F)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

    if os.path.isdir('./school/'+school.name):
        to = open('./school/'+school.name+'/total.gf', 'r')
        total = to.readline()
        total = float(total.strip('\n'))    
        if os.path.isfile('./school/'+school.name+'/'+y+m+d+'.gf'):
            t = open('./school/'+school.name+'/'+y+m+d+'.gf','r')
            re = t.readline()
            re = float(re.strip('\n'))
            embed.set_footer(text='이 급식의 평점:'+str(re)+" 학교 전체 평점:"+str(total))
            t.close()
        else:
            embed.set_footer(text="이급식의 평점:없음  학교 전체 평점:"+str(total))
            to.close()
    else:
        embed.set_footer(text="이 급식의 평점 없음  학교 전체 평점:없음")
    await p.delete()
    send = await ctx.channel.send(embed=embed)  
###############################################################################################

#################################################별점##########################################
    if y==str(date.year) and m==str(date.month) and d==str(date.day) and content == 1 and datetime.today().hour >= 12:
        emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣','❌']
        for i in range(6):
            await send.add_reaction(emoji[i])

        def emocheck(reaction):
            if reaction.user_id == ctx.author.id and reaction.emoji.name in emoji and reaction.message_id == send.id:
                return T

        try:
            reaction = await client.wait_for(event='raw_reaction_add', timout = 15, check = emocheck)
        except asyncio.TimeoutError:
            await send.delete()
            await ctx.channel.send(embed=embed)
        else:
            if reaction.emoji.name != '❌':
                review.review(reaction,school.name,y,m,d,str(ctx.author))
            await send.delete()
            await ctx.channel.send(embed=embed)
################################################################################################
    del author[author.index(ctx.author)]
    
@client.command(name='별칭')  # 별칭 기능
async def short(ctx, origin, new):
    '''This funtion is that shorts origin name to custom name'''
    path = './user/'+str(ctx.author)+'/shorts/'  # 경로 지정
    os.makedirs(path, exist_ok=T)  # 폴더 생정
    p = open(path+str(new)+'.gf', 'w')  # 파일 오픈
    p.write(str(origin))  # 쓰기
    await ctx.channel.send('줄이기 성공:'+origin + '->' + new)  # 메세지 출력


@short.error  # 줄이기 에러가 날 경우
async def error(ctx, error):
    await ctx.channel.send("제대로 입력해주세요")

@급식.error
async def error(ctx, error):
    await ctx.channel.send("제대로 입력해주세요")
    del author[author.index(ctx.author)]


@client.event  # 에러가 날경우
async def on_command_error(ctx, error):
    pass


os.makedirs('./school', exist_ok=T)  # 폴더 만들기
os.makedirs('./user', exist_ok=T)  # 폴더 만들기
client.run(token)  # token 값을 가진 봇을 구동
