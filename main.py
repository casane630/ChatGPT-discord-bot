import discord
import cgpt
import os
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
edit=""
@client.event
async def on_message(message):
    userData = str(message.author.id) + ":Data"
    userMode = str(message.author.id) + ":ModeFlag"
    userEdit = str(message.author.id) + ":Edit"
    userMessage = str(message.author.id) + ":Message"
    if userData not in globals():
        globals()[userData] = [
            {"role": "system", "content": "あなたは会話に日本語で返答するアシスタントです。"},
            {"role": "system", "content": "あなたは一つの題材についてだけ答えます"}
        ]
    if userMessage not in globals():
        globals()[userMessage] = []
    if userEdit not in globals():
        globals()[userEdit] = ""
    if userMode not in globals():
        globals()[userMode] = 0
    if message.author.bot:
        return
    if message.content == '.exit' and globals()[userMode]==1:
        await message.delete()
        globals()[userMode]=0
        embed = discord.Embed(title="ChatGPT",description="",color=0xff0000)
        for i in range(0, len(globals()[userMessage]), 2):
            title="\n"+globals()[userMessage][i]+":"
            embed.add_field(name=title,value=globals()[userMessage][i+1],inline=False)
        await globals()[userEdit].edit(embed=embed)
    if globals()[userMode] == 1:
        await message.delete()
        userData = str(message.author.id) + ":Data"
        data = globals()[userData]
        data.append({"role": "user", "content": message.content})
        globals()[userMessage].append(message.content)
        globals()[userMessage].append(cgpt.cgpt(data))
        embed = discord.Embed(title="ChatGPT",description="",color=0x00ff00)
        for i in range(0, len(globals()[userMessage]), 2):
            title="\n"+globals()[userMessage][i]+":"
            embed.add_field(name=title,value=globals()[userMessage][i+1],inline=False)
        await globals()[userEdit].edit(embed=embed)
    if message.content == '.cgpt' and globals()[userEdit]!=1:
        await message.delete()
        if userData in globals():
            del globals()[userData]
        if userMessage in globals():
            del globals()[userMessage]
        globals()[userMode]=1
        embed = discord.Embed(title="ChatGPT",description="「.exit」で終了",color=0x00ff00)
        globals()[userEdit] = await message.channel.send(embed=embed)
client.run(os.environ['discordToken'])
