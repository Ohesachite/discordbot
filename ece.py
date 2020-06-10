import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='stink ')
TOKEN = ''
os.environ.get(TOKEN)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game("Stinking the ECE Building"))

@bot.command(name='ece', help='Stinky ECE majors!')
async def uh_oh(ctx):
    await ctx.send('Uh oh! Stinky!')

@bot.command(name='Ece', help='Stinky ECE majors!')
async def uh_oh_cap(ctx):
    await ctx.send('Uh oh! Stinky!')

@bot.command(name='ECE', help='Stinky ECE majors!')
async def uh_oh_upper(ctx):
    await ctx.send('Uh oh! Stinky!')

@bot.command(name='add', help='Add group chat for class')
async def add_class(ctx, subject, course_number):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name = subject.upper() + ' ' + course_number)
    if(role is None):
        await ctx.send('Not a class on this server!')
    else:
        await user.add_roles(role)
        await ctx.send('Class added!')

@bot.command(name='remove', help='Remove group chat for class')
async def remove_class(ctx, subject, course_number):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name = subject.upper() + ' ' + course_number)
    if(role is None):
        await ctx.send('Not a class on this server!')
    elif role in user.roles:
        await user.remove_roles(role)
        await ctx.send('Class removed!')
    else:
        await ctx.send('You are not in the class!')

@bot.command(name='create', help='Create class on this server, contains additional arguments (d,l,av) which must be specified after the class name, command accessible only to admins or mods')
@commands.has_permissions(manage_channels=True)
async def create_class(ctx, subject, course_number, *args):
    g = ctx.guild
    n = subject.upper() + ' ' + course_number
    if not (discord.utils.get(g.roles, name = n) is None):
        await ctx.send('Class already exists: ' + n)
        return
    role = await g.create_role(name=n)
    overwrites = {
        g.default_role: discord.PermissionOverwrite(read_messages=False),
        discord.utils.get(g.roles, name = 'Admin'): discord.PermissionOverwrite(read_messages=True),
        discord.utils.get(g.roles, name = 'Moderators'): discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    category = await g.create_category(n, overwrites = overwrites)
    await g.create_text_channel('everythingelse', category = category)
    await g.create_text_channel('homework', category = category)
    await g.create_text_channel('exams', category = category)
    if 'd' in args:
        await g.create_text_channel('discussion', category = category)
    if 'l' in args:
        await g.create_text_channel('labs', category = category)
    await g.create_voice_channel('general', category = category)
    if 'av' in args:
        if 'd' in args:
            await g.create_voice_channel('discussion', category = category)
        if 'l' in args:
            await g.create_voice_channel('labs', category = category)
    await ctx.send('Created new class: ' + n)
    print(len(g.channels))

@bot.command(name='edit', help='Edit class on server using arguments (d,l,av), command accessible only to admins or mods')
@commands.has_permissions(manage_channels=True)
async def edit_class(ctx, subject, course_number, *args):
    g = ctx.guild
    n = subject.upper() + ' ' + course_number
    role = discord.utils.get(g.roles, name=n)
    if role is None:
       await ctx.send('Class does not exist!')
       return
    category = discord.utils.get(g.categories, name=n)
    dchannel = discord.utils.get(category.channels, name='discussion')
    if ('d' in args) and (dchannel is None):
        await g.create_text_channel('discussion', category=category)
    elif (not ('d' in args)) and (not (dchannel is None)):
        await dchannel.delete()
    lchannel = discord.utils.get(category.channels, name='labs')
    if ('l' in args) and (lchannel is None):
        await g.create_text_channel('labs', category=category)
    elif (not ('l' in args)) and (not (lchannel is None)):
        await lchannel.delete()
    for vc in category.voice_channels:
        if not (vc.name == 'general'):
            await vc.delete()
    if 'av' in args:
        if 'd' in args:
            await g.create_voice_channel('discussion', category = category)
        if 'l' in args:
            await g.create_voice_channel('labs', category = category)
    await ctx.send('Edited class: ' + n)
    print(len(g.channels))

@bot.command(name='delete', help='Delete class on this server, command accessible only to admins or mods')
@commands.has_permissions(manage_channels=True)
async def delete_class(ctx, subject, course_number):
    g = ctx.guild
    n = subject.upper() + ' ' + course_number
    role = discord.utils.get(g.roles, name=n)
    if role is None:
        await ctx.send('Class does not exist!')
        return
    category = discord.utils.get(g.categories, name=n)
    for channel in category.channels:
        await channel.delete()
    await category.delete()
    await role.delete()
    await ctx.send('Class deleted: ' + n)
    print(len(g.channels))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Not enough parameters!')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found!')
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send('You do not have permission!')
    else:
        raise error

bot.run(TOKEN)
