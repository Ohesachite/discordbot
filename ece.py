import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='stink ')
os.environ.get('')

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Not enough parameters!')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found!')
    else:
        raise error

bot.run('')
