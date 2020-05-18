import discord
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

@client.event
async def on_ready():
    perms = discord.Permissions(268435456)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    roles = message.guild.roles
    cont = message.content

    if cont.lower() == 'ece' or cont.lower() == 'ee' or cont.lower() == 'ce' or cont.lower() == 'compe':
        await message.channel.send('Uh oh! Stinky!')

    contparts = cont.split()
    if(contparts[0] == 'stink'):
        if(len(contparts) == 1):
            await message.channel.send('Usage: stink [command] [paramaters]')
        elif(contparts[1] == 'add'):
            if(len(contparts) == 2):
                await message.channel.send('Usage: stink add [subject] [number]')
            elif(len(contparts) == 4):
                role = find_role(roles, contparts[2] + ' ' + contparts[3])
                if(role == None):
                    await message.channel.send('Class not found! Please check with an admin if that class actually exists!')
                else:
                    await client.add_roles(message.author, role)

        else:
            await message.channel.send('Invalid command!')

client.run('')
