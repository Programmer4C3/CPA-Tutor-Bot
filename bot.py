import discord
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

load_dotenv()

token = os.getenv("DISCORD_BOT_TOKEN")
commandsFile = None
guildInfo = None

with open("commands.JSON") as f:
    commandsFile = json.load(f)

with open("guildInfo.JSON") as f:
    guildInfo = json.load(f) 

def loadGuildInfo():
    with open("guildInfo.JSON") as f:
        guildInfo = json.load(f) 
        return guildInfo

loadGuildInfo()

if commandsFile == None or guildInfo == None or token == None:
    print("File Loading Unsuccessful!")
    quit()

async def isCommand(Msg):
    greetings_array = commandsFile["Greetings"]
    salutations_array = commandsFile["Salutations"]
    commands_array = commandsFile["Commands"]
    
    if Msg.content[0] == guildInfo["commandPrefix"]:
        for i in range(0,len(commands_array)):
            if (Msg.content.lower().split()[0])[1:] == commands_array[i]:
                #Compute Command
                if i == 3:
                    computation = Msg.content.lower().split()
                    if len(computation) >= 4:
                        try:
                            num1 = int(computation[1])
                            operator = computation[2]
                            num2 = int(computation[3])
                            result = "Operation Issue"
                            if num1 <= 10 and num2 <= 10:
                                await Msg.channel.send("Dumbass you can't do basic math?")
                                return 1
                            if operator == "+":
                                result = num1+num2
                            elif operator == "-":
                                result = num1-num2
                            elif operator == "x":
                                result = num1*num2
                            await Msg.channel.send(f"The answer is: `{result}`")
                            
                        except ValueError:
                            await Msg.channel.send("are you sure your [num1] and [num2] are numbers?")
                    else:
                        await Msg.channel.send("The correct format is for the command **.compute** is:\n`.compute num1 operator num2`")
                #Die command, it basically kills the running bot (ONLY RUN FOR EMERGENCY)
                elif i == 4:
                    return 2
                else:
                    await Msg.channel.send(f"The {commands_array[i]} command is still being coded. Sadly")
                return 1
        await Msg.channel.send(f"Are you sure that's a proper command?\nRun `listCMD' to display all the commands")
        return 0
            
            

def getTime():
    currentTime = datetime.now().time()
    if currentTime.hour > 12:
        return (f"{currentTime.hour-12}:{currentTime.minute} PM")
    elif currentTime == 12:
     return (f"{currentTime.hour}:{currentTime.minute} PM")
    else:
       return (f"{currentTime.hour}:{currentTime.minute} AM")

def saveGuildInfo(newGuildInfo):
    with open("guildInfo.JSON", "w") as f:
        json.dump(newGuildInfo, f, indent=4)
    
def addGuild(data):
    currentGuildData = loadGuildInfo()
    currentGuildData[data] = {
        "CommandPrefix":".",
        "BotChannel": 0,
        "WelcomeChannel": 0
    }
    saveGuildInfo(currentGuildData)

def leaveGuild(data):
    currentGuildData = loadGuildInfo()
    currentGuildData.pop(data,None)
    saveGuildInfo(currentGuildData)


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'The Study Machine is now Online!')
        for guild in client.guilds:
            if not (str(guild.id) in guildInfo):
                addGuild(str(guild.id))
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        await channel.send("Initialized Config Settings")
                        break

    async def on_guild_join(self, guild):
        print("joined")
    
    async def on_guild_remove(self, guild):
        print("left")

    async def on_message(self, message):
        try:
            if message.author == self.user:
                return
            
            commandRunner = await isCommand(message)
            
            if commandRunner == 1:
                print(f'[{getTime()}] {message.author}: {message.content} [CMD]')
            elif commandRunner == 2:
                if message.author.id == 8550831592497479880:
                    await message.channel.send("You have just killed the running process")
                    await self.close()
                else:
                    await message.channel.send("Currently only **Abishak** can run that command")
            else:
                print(f'[{getTime()}] {message.author}: {message.content} [REG]')
        except Exception as e:
            print(f"DUMBASS YOU CAUSED A ERROR {Exception}")
            quit()

        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

try:
    client.run(token)
except KeyboardInterrupt:
    sys.exit(0)