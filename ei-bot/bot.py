#discord imports
import os
import discord
import sqlite3
import ei_funct as ef

from discord import app_commands
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv


#ei imports
import requests
import ei_pb2
import base64

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
user_id = os.getenv('USER_ID')



def create_table():
    
    cur = db.cursor()
    #Table Creation
    cur.execute('''
    CREATE TABLE IF NOT EXISTS kappaINFO (
        id integer PRIMARY KEY AUTOINCREMENT,
        eid text NOT NULL,
        username text NOT NULL
        )
    ''')
    db.commit()


bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())
db = sqlite3.connect('ei-bot/ei-db/kappa.db')

create_table()



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    try:
        synced = await bot.tree.sync()
        print("Synced")
    except Exception as e:
        print(e)




@bot.tree.command(name="join")
@app_commands.describe(eid = "Enter EID")
async def join(interaction: discord.Interaction, eid: str):

    namecheck = db.execute("SELECT * FROM kappaINFO WHERE username=?", (interaction.user.name,))
    rows = namecheck.fetchall()

    if rows:
        await interaction.response.send_message(f"The user {interaction.user.name} has already joined.")
    
    else:

        try:
            periodicals_request = ei_pb2.EggIncFirstContactRequest()
            periodicals_request.ei_user_id = eid
            periodicals_request.client_version = 42

            url = 'https://www.auxbrain.com/ei/bot_first_contact' 
            data = { 'data' : base64.b64encode(periodicals_request.SerializeToString()).decode('utf-8') }
            response = requests.post(url, data = data)
            response.raise_for_status()
            
            periodicals_response = ei_pb2.EggIncFirstContactResponse()
            periodicals_response.ParseFromString(base64.b64decode(response.text))

            # Check for errors in the response
            if periodicals_response.backup.user_name == "":
                raise Exception     

        except Exception as e:
            await interaction.response.send_message("EID is incorrect or problems with server")
            return
            
        cur = db.cursor()    
        cur.execute('''
            INSERT INTO kappaINFO (eid, username) 
            VALUES (?, ?)
        ''', (eid, interaction.user.name))
        db.commit()
        await interaction.response.send_message(f"The user {interaction.user.name} has joined successfully.")




@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):

    namecheck = db.execute("SELECT eid FROM kappaINFO WHERE username=?", (interaction.user.name,))
    row = namecheck.fetchone()

    if row is not None:

        user_id = row[0] 

        periodicals_request = ei_pb2.EggIncFirstContactRequest()
        periodicals_request.ei_user_id = user_id
        periodicals_request.client_version = 42

        url = 'https://www.auxbrain.com/ei/bot_first_contact' 
        data = { 'data' : base64.b64encode(periodicals_request.SerializeToString()).decode('utf-8') }
        response = requests.post(url, data = data)

        periodicals_response = ei_pb2.EggIncFirstContactResponse()
        periodicals_response.ParseFromString(base64.b64decode(response.text))

        ## Get Soul Egg amount and convert to readable form
        total_soul = ef.numer_formatter(periodicals_response.backup.game.soul_eggs_d)

        ## Embed discord text bubble
        embed = Embed(title="Egg Inc Profile",description="A amazingly amazing description of your current egg inc", color=0xffd700)  
        embed.add_field(name="Discord User", value=interaction.user.name, inline=False)
        embed.add_field(name="Egg Inc IGN", value=periodicals_response.backup.user_name, inline=False)                                   
        embed.add_field(name="Soul Eggs", value=total_soul, inline=False)
        embed.add_field(name="Prophecy Eggs", value=periodicals_response.backup.game.eggs_of_prophecy, inline=False)


        await interaction.response.send_message(embed=embed,ephemeral=True)


    else:
        await interaction.response.send_message(f"The user {interaction.user.name} has not yet joined to be able to use this command.")





    

bot.run(TOKEN)

