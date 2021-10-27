import discord
from discord.http import Route

bot = discord.Client()
http = bot.http

default_components = [
    {
        "type": 1,
        "components": [
            {
                "type": 2,
                "label": "Python",
                "style": 2,
                "custom_id": "python",
                "emoji": {
                    "id": "847876880257908757",
                    "name": "python"
                }
            }, {
                "type": 2,
                "label": "Kotlin",
                "style": 2,
                "custom_id": "kotlin",
                "emoji": {
                    "id": "847876848662216714",
                    "name": "kotlin"
                }
            }, {
                "type": 2,
                "label": "C언어",
                "style": 2,
                "custom_id": "c"
            }, {
                "type": 2,
                "label": "C++",
                "style": 2,
                "custom_id": "cpp",
                "emoji": {
                    "id": "847876987778629722",
                    "name": "cpp"
                }
            }, {
                "type": 2,
                "label": "Java",
                "style": 2,
                "custom_id": "java",
                "emoji": {
                    "id": "847876915619954708",
                    "name": "java"
                }
            }
        ]

    }
]

@bot.event
async def on_message(msg: discord.Message):
	if msg.content == "!프로그래밍":
		embed = discord.Embed(
			title="최고의 프로그래밍 언어",
			description="""<:python:847876880257908757> Python: 0표
				<:kotlin:847876848662216714> Kotlin: 0표
				C언어: 0표
				<:cpp:847876987778629722> C++: 0표
				<:java:847876915619954708> Java: 0표""",
			colour=0x0080ff
		)
        
		r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
		payload = {
			"embed": embed.to_dict()
			"components": default_components
		}
		http.request(r, json=payload)
		return
       
bot.run("NzczNDQzMjI1NDI3NjQwMzIw.X6JTIg.-RPsiocdBvZslvOvWX0PqXVX5G8")