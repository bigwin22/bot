import asyncio
import discord
from discord.ext import commands

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

# 봇이 특정 메세지를 받고 인식하는 코드
@client.command()
async def 급식(ctx,type,name,year,month,day):


    await ctx.send()

async def 타이머(ctx, *text):


client.run(token)