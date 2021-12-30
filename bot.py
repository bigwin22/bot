import asyncio
import discord
from datetime import datetime
from discord.client import Client
from discord.ext import commands
from pytz import timezone
import os

# 내가 만들 모듈
import module.School as Sinfo  #학교 기본 정보
import module.review as review #리뷰 기능 모듈
import module.logger as log    #로그 작성 모듈
from define_class import Today #오늘 날짜 정보 클래스
from define_class import School#학교 정보 클래스

# 학교코드:7041189

client = commands.Bot(command_prefix='!')  # 명령어 호출 코드
F = False
T = True

KST = timezone('Asia/Seoul')#시간대 설정
print(datetime.now(KST))

# 생성된 토큰을 입력해준다.
token = open('token.token', 'r')
token = str(token.readline())

# 봇이 구동되었을 때 보여지는 코드


@client.event
async def on_ready():
    '''봇이 준비 되었을 때'''
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")

author = []  # 입력한 유저의 정보 저장

# 급식 명령어
@client.command()
async def 급식(ctx, *val):  # ctx:디스코드 채팅 정보, val:명령의 뒤에 붙는 값들 (ex:이름,년,월,일)
    '''급식 값을 얻은 후 임베드 형식으로 출력'''
    def printf(title, year, month, day):
        '''임베드 추가 함수'''
        # 임메드 값 추가를 return
        return discord.Embed(title=title, description=year+' '+month+' '+day, color=0x62c1cc)

    log.entered(str(ctx.author),val,str(ctx.author))#로그 시스템
    log.fstarting('command Func', str(ctx.author))
    date = datetime.now(KST)
##################################################처리 시작 코드#######################
    log.fstarting('start code',str(ctx.author))
    fpath = "./user/"+str(ctx.author)
    os.makedirs(fpath, exist_ok=T)  # fpath 경로에 폴더가 존재하지 않을 시 생성
    os.makedirs(fpath+'/review', exist_ok=T)

    if (ctx.author in author):  # 같은 사람이 두 개의 이상의 값을 동시에 처리할 경우 무시
        log.custom("User already entered", ctx.author)
        await ctx.channel.send("이미 처리 중이에요")
        return
    author.append(ctx.author)  # 유저 정보 추가

    p = await ctx.channel.send("처리 중입니다..........")
    log.fend('start code',str(ctx.author))
#######################################################################################

###################################################기본 세팅(변수,함수)##########################
    log.fstarting('initial Func',str(ctx.author))
    school = School()#학교 기본 정보를 클래스 형식으로 구성
    
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
    
    store = []#급식 값 저장할 리스트 변수
    log.fend('initial Func',str(ctx.author))
 ##################################################################################### 

#######################################경우에 수에 따른 변수 값 지정#####################
    log.fstarting('variable code',str(ctx.author))
    if len(val) == 0:#명령어 뒤에 아무것도 입력 안될 대
        if os.path.isfile(fpath+'/name.gf'):
            f = open(fpath+'/name.gf', 'r')
            em = f.readline()
            school.name = em
            f.close()

            f = open(fpath+'/code.gf', 'r')
            em = f.readline()
            school.area = em[0:3]#교육청 코드
            school.code = em[3:] #학교 고유 코드
            f.close()
        else:
            await p.delete()
            await ctx.channel.send("마지막으로 입력된 학교가 없습니다.")
            del author[author.index(ctx.author)]
            return
    elif len(val) > 0:#명령어 뒤에 입력된 것이 있을 때
        if os.path.isfile('./user/'+str(ctx.author)+'/shorts/'+val[0]+'.gf'):#입력한 학교가 줄임말 파일과 같을 경우
            f = open('./user/'+str(ctx.author)+'/shorts/'+val[0]+'.gf','r')
            school.school(str(f.readline()),-1)
        else:
            school.school(val[0],-1)
        
        if len(school.name) > 10:#유저가 입력한 글자가 들어간 학교가 너무 많으면
            del author[author.index(ctx.author)]
            await p.delete()
            await ctx.channel.send("해당하는 학교가 너무 많습니다. 좀 더 정확히 입력해주세요")
            return
        if len(school.name) > 1:#학교 갯수가 2개 이상일 경우
            clist = []
            cprint = []
            for i in range(len(school.name)):#선택지 추가
                clist.append(i+1)
                cprint.append(await ctx.channel.send("```"+str(i+1)+":"+school.name[i]+'('+school.add[i]+')'+"```"))
            a = await ctx.channel.send("(번호)로 입력해주세요 ``예: 1``")

            try:
                msg = await client.wait_for('message', timeout=len(school.name)+6, check=check)
            except asyncio.TimeoutError:#시간초과 날 경우
                for i in range(len(cprint)):#출력한 선택지 지우기
                    await cprint[i].delete()
                await a.delete()#지우기
                await p.delete()#지우기
                await ctx.channel.send(ctx.author.mention+" 선택지 시간 초과")
                del author[author.index(ctx.author)]
                return
            else:#잘 입력 되었을 때
                school.setting(choice)#학교 정보 구성
                for i in range(len(cprint)):#출력 메시지 지우기
                    await cprint[i].delete()
                await a.delete()
        else:#학교 갯수가 한개면
            school.setting(0)   
    log.fend('variable code', str(ctx.author))            
###################################################################################################

##############################################급식 정보###########################################
    log.fstarting('processing code', str(ctx.author))
    today = Today(val)#현재 날짜
    embed = printf(school.name, today.y,today.m,today.d)#임베드 값설정
    y = today.y#년  
    m = today.m#월
    d = today.d#일

    for i in range(3):#급식 정보 구하기
        log.fstarting('process Func',str(ctx.author))
        store.append(Sinfo.food(school.area,school.code,i+1,y+m+d))
        log.fend('process Func', str(ctx.author))
    log.custom(f"Value of variable of 'store' is {store}",str(ctx.author))
    f = open(fpath+"/name.gf", 'w')#유저의 데이터 기록
    f.write(school.name)    
    f.close()

    f = open(fpath+"/code.gf",'w')
    f.write(school.area+school.code)
    f.close()
    log.fend('processing code',str(ctx.author))
##################################################################################################

######################################급식 정보 출력##################################################
    log.fstarting('print code', str(ctx.author))
    when = ['아침','점심','저녁']
    content = 0
    for i in range(3):#급식 값 존재 여부 판단
        if store[i] != '없음':
            content = 1
        embed.add_field(name=when[i],value=store[i],inline=F)#임베드 값 추가
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)#호출한 유저의 값을 임베드에 추가

    if os.path.isdir('./school/'+school.name):#학교의 리뷰 파일이 있으면 임베드에 추가
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
    send = await ctx.channel.send(embed=embed) #임베드 출력
    log.fend('print code', str(ctx.author))
###############################################################################################

#################################################별점##########################################
    log.fstarting('review code',str(ctx.author))
    if y==str(date.year) and m==str(date.month) and d==str(date.day) and content == 1 and datetime.now(KST).hour >= 12:
        emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣','❌']
        for i in range(6):#이모지 출력
            await send.add_reaction(emoji[i])

        def emocheck(reaction):#이모지 입력 여부 판단 함수
            if reaction.user_id == ctx.author.id and reaction.emoji.name in emoji and reaction.message_id == send.id:
                return T

        try:
            reaction = await client.wait_for(event='raw_reaction_add', timeout = 15, check = emocheck)
        except asyncio.TimeoutError:#시간 초과
            await send.delete()
            await ctx.channel.send(embed=embed)#임베드 재 출력
        else:
            if reaction.emoji.name != '❌':
                review.review(reaction,school.name,y,m,d,str(ctx.author))
            await send.delete()
            await ctx.channel.send(embed=embed)
    log.fend('review code',str(ctx.author))
################################################################################################
    del author[author.index(ctx.author)]
    log.fend('command Func', str(ctx.author))

@client.command(name='별칭')  # 별칭 기능
async def short(ctx, origin, new):
    '''이 함수는 학교 이름을 유저가 원하는 이름으로 바꿔줍니다.'''
    log.entered(ctx.author,(origin,new))
    log.fstarting('short',ctx.author)
    path = './user/'+str(ctx.author)+'/shorts/'  # 경로 지정
    os.makedirs(path, exist_ok=T)  # 폴더 생정
    p = open(path+str(new)+'.gf', 'w')  # 파일 오픈
    p.write(str(origin))  # 쓰기
    await ctx.channel.send('줄이기 성공:'+origin + '->' + new)  # 메세지 출력
    log.custom('줄이기 성공:'+origin + '->' + new,ctx.author)
    log.fend('short',ctx.author)


@short.error  # 줄이기 에러가 날 경우
async def error(ctx, error):
    await ctx.channel.send("제대로 입력해주세요")
    log.custom(f'에러발생:short({error})',ctx.author)

@급식.error
async def error(ctx, error):
    await ctx.channel.send("제대로 입력해주세요")
    del author[author.index(ctx.author)]
    log.custom(f'에러발생:급식({error})',ctx.author)


@client.event  # 에러가 날경우
async def on_command_error(ctx, error):
    pass

os.makedirs('./school', exist_ok=T)  # 폴더 만들기
os.makedirs('./user', exist_ok=T)  # 폴더 만들기
client.run(token)  # token 값을 가진 봇을 구동
