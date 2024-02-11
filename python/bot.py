import os
import discord
import sqlite3

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
user_id = os.getenv('USER_ID')

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())
db = sqlite3.connect('kappa.db')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    try:
        synced = await bot.tree.sync()
        print("Synced")
    except Exception as e:
        print(e)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Sup homie {member.name}')


@bot.tree.command(name="join")
@app_commands.describe(eid = "Enter EID")
async def join(interaction: discord.Interaction, eid: str):
    await interaction.response.send_message(eid)


bot.run(TOKEN)

