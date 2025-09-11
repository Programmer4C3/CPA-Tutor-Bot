import discord
import json
from datetime import datetime
import os

token = os.getenv("DISCORD_BOT_TOKEN")
commandsFile = None
botInfo = None

with open("commands.JSON") as f:
    commandsFile = json.load(f)

with open("botInfo.JSON") as f:
    botInfo = json.load(f) 

if commandsFile == None or botInfo == None or token == None:
    print("File Loading Unsuccessful!")
    quit()

async def isCommand(Msg):
    greetings_array = commandsFile["Greetings"]
    salutations_array = commandsFile["Salutations"]
    commands_array = commandsFile["Commands"]
    
    if Msg.content[0] == botInfo["commandPrefix"]:
        for i in range(0,len(commands_array)):
            if (Msg.content.lower().split()[0])[1:] == commands_array[i]:
                await Msg.channel.send(f"You just ran the {commands_array[i]} command")
                return True

def getTime():
    currentTime = datetime.now().time()
    if currentTime.hour > 12:
        return (f"{currentTime.hour-12}:{currentTime.minute} PM")
    elif currentTime == 12:
     return (f"{currentTime.hour}:{currentTime.minute} PM")
    else:
       return (f"{currentTime.hour}:{currentTime.minute} AM")

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    try:
        async def on_message(self, message):
            if message.author == self.user:
                return
            
            if await isCommand(message):
                print(f'[{getTime()}] {message.author}: {message.content} [CMD]')
            else:
                print(f'[{getTime()}] {message.author}: {message.content} [REG]')
    except Exception as e:
        print(f"DUMBASS YOU CAUSED A ERROR {Exception}")
        quit()

        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(token)