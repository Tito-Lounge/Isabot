import discord
from config import TOKEN
import time
import os
import pandas as pd
import json
from discord.ext import commands, tasks
import asyncio

id = '<@1166119876503556136>'
intents = discord.Intents.all()
client = commands.Bot(command_prefix='i$', intents = intents)
client.remove_command('help')

# File Initialization & Variable Declaration:
global start_time
if os.path.exists('./start_time.txt'):
    with open('./start_time.txt', 'r') as f:
        start_time = float(f.read())
else:
    start_time = time.time()
    with open(f'./start_time.txt', 'w') as f:
        f.write(str(start_time))

if not os.path.exists('./data.csv'):
    data = pd.DataFrame(columns=['Duration', 'Break Statement'])
    data.to_csv('data.csv', index = False)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Commands 
@client.command(name='streak') # Outputs time elapsed since last mean thing said.
async def streak(ctx):
    current_time = time.time()
    elapsed_time = current_time - start_time
    days = elapsed_time // 86400
    hours = (elapsed_time // 3600) % 24
    minutes = (elapsed_time // 60) % 60
    seconds = elapsed_time % 60
    await ctx.send(f"Isabelle has not been mean to Eric for **{int(days)}** days, **{int(hours)}** hours, **{int(minutes)}** minutes & **{int(seconds)}** seconds!")

@client.command(name='mean') # Reports a mean incident, appends the current streak to ledger and resets it. 
async def mean(ctx, *, message: str):
    global start_time, df
    current_time = time.time()
    elapsed_time = current_time - start_time
    days = elapsed_time // 86400
    hours = (elapsed_time // 3600) % 24
    minutes = (elapsed_time // 60) % 60
    seconds = elapsed_time % 60
    
    # Append streak to ledger
    new_row = {'Duration': elapsed_time, 'Break Statement': message}
    row_df = pd.DataFrame([new_row])
    row_df.to_csv('data.csv', mode='a', header = False, index = False)

    # Reset timer
    if os.path.exists('start_time.txt'):
        with open('start_time.txt', 'r') as f:
            os.remove('start_time.txt')
    start_time = time.time()
    with open(f'start_time.txt', 'w') as f:
        f.write(str(start_time))
    
    await ctx.send(f'Isabelle ended her nice-streak of **{int(days)}** days, **{int(hours)}** hours, **{int(minutes)}** minutes & **{int(seconds)}** seconds by saying \"{message}\".')

@client.command(name='longest') # Outputs the the longest streak from the ledger.
async def longest(ctx):
    global start_time
    elapsed_time = time.time() - start_time
    with open('data.csv', 'r') as file:
        df = pd.read_csv('./data.csv')
        longest_time = float(df['Duration'].max())
        longest_statement = df.loc[df['Duration'].idxmax()]['Break Statement']
        days = longest_time // 86400
        hours = (longest_time // 3600) % 24
        minutes = (longest_time // 60) % 60
        seconds = longest_time % 60
    print(elapsed_time)
    print(longest_time)
    if (elapsed_time > longest_time):
        await ctx.send('This is currently the longest Isabelle has been nice to Eric.')
    else:
        await ctx.send(f'The longest Isabelle has been nice to Eric was for **{int(days)}** days, **{int(hours)}** hours, **{int(minutes)}** minutes & **{int(seconds)}** seconds and she broke her nice-streak by saying \"{longest_statement}\"')

@client.command(name = 'help')
async def help(ctx):
    embed=discord.Embed(title="__**Command List**__", description="⏳ hi chat i think it would actually kill her to be nice to me ⏳", color=0xffb2d8)
    embed.add_field(name="💗 i$help", value="...", inline=False)
    embed.add_field(name="💗 i$streak", value="*Shows the duration of the current nice-streak.*", inline=False)
    embed.add_field(name="💗 i$mean [message]", value="*Ends the nice-streak and appends the duration and what she said in [message] to the ledger.*", inline=False)
    embed.add_field(name="💗 i$longest", value="*Shows the longest streak and what was said to end it.*", inline=True)
    await ctx.send(embed=embed)

client.run(TOKEN)

