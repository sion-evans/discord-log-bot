import discord
import json

filename = "config.json"

client = discord.Client()

with open(filename) as json_file:
    config = json.load(json_file)

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} is connected to: {guild.name}')

@client.event
async def on_message(message):
    if '!toggle' == message.content.lower() and config["owner"] == message.author.id:
        if message.channel.id not in config["channel"]:
            config["channel"].append(message.channel.id)
            with open(filename, 'w') as json_file:
                json.dump(config, json_file)
            await message.channel.send("Added.")
        else:
            config["channel"].remove(message.channel.id)
            with open(filename, 'w') as json_file:
                json.dump(config, json_file)
            await message.channel.send("Removed.")

@client.event
async def on_member_join(member):
    for x in config["channel"]:
        try:
            channel = client.get_channel(x)
            await channel.send(f'{member.name} joined the server.')
        except Exception as error:
            print("Error: ", error)
            config["channel"].remove(x)

@client.event
async def on_member_remove(member):
    for x in config["channel"]: 
        try:
            channel = client.get_channel(x)
            await channel.send(f'{member.name} left the server.')
        except Exception as error:
            print("Error: ", error)
            config["channel"].remove(x)

@client.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        for x in config["channel"]:
            try:
                channel = client.get_channel(x)
                if after.nick is not None:
                    await channel.send(f'{before.name} changed his/her nickname to {after.nick}.')
                else:
                    await channel.send(f'{before.name} removed his/her nickname.')
            except Exception as error:
                print("Error: ", error)
                config["channel"].remove(x)

@client.event
async def on_voice_state_update(member, before, after):
    for x in config["channel"]:
        try:
            channel = client.get_channel(x)
            if before.channel is None and after.channel is not None:
                await channel.send(f'{member.name} joined {after.channel.name}.')
            elif after.channel is None and before.channel is not None:
                await channel.send(f'{member.name} left {before.channel.name}.')
            elif before.channel is not None and after.channel is not None:
                if before.channel.id != after.channel.id:
                    await channel.send(f'{member.name} moved to {after.channel.name}.')
        except Exception as error:
            print("Error: ", error)
            config["channel"].remove(x)

client.run(config["token"])
