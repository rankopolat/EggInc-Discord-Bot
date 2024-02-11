#discord imports
import os
import discord
import sqlite3
import ei_funct as ef

#from discord imports
from discord import app_commands
from discord import Embed
from discord.ext import commands

#.env import
from dotenv import load_dotenv

#ei imports
import requests
import ei_pb2
import base64



# Load env file gathering Discord Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



#Create egg inc main command bot
bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

# Connect To the sqlite Database
db = sqlite3.connect('ei-bot/ei-db/kappa.db')
#Create db Table if not exists
ef.create_table(db)

###Successful Bot Sync Check
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    try:
        synced = await bot.tree.sync()
        print("Synced")
    except Exception as e:
        print(e)





### /Join command entering EID# to register into the DB
@bot.tree.command(name="join")
@app_commands.describe(eid = "Enter EID")
async def join(interaction: discord.Interaction, eid: str):

    namecheck = db.execute("SELECT * FROM kappaINFO WHERE username=?", (interaction.user.name,))
    rows = namecheck.fetchall()

    if rows:
        await interaction.response.send_message(f"The user {interaction.user.name} has already joined.")
    
    else:

        periodicals_request = ei_pb2.EggIncFirstContactRequest()
        periodicals_request.ei_user_id = eid
        periodicals_request.client_version = 42

        url = 'https://www.auxbrain.com/ei/bot_first_contact' 
        data = { 'data' : base64.b64encode(periodicals_request.SerializeToString()).decode('utf-8') }
        response = requests.post(url, data = data)
        response.raise_for_status()
        
        periodicals_response = ei_pb2.EggIncFirstContactResponse()
        periodicals_response.ParseFromString(base64.b64decode(response.text))
        
        try:
            # Check for errors in the response
            if periodicals_response.backup.user_name == "":
                raise Exception     

        except Exception as e:
            await interaction.response.send_message("EID is incorrect or problems with server")
            return
        

        total_eb = ef.calc_earning_bonus(periodicals_response)

        cur = db.cursor()    
        cur.execute('''
            INSERT INTO kappaINFO (eid, username,soul_eggs,proph_eggs,earning_bonus) 
            VALUES (?, ?, ?, ?, ?)
        ''', (eid, interaction.user.name,periodicals_response.backup.game.soul_eggs_d,periodicals_response.backup.game.eggs_of_prophecy, total_eb))

        db.commit()

        await interaction.response.send_message(f"The user {interaction.user.name} has joined successfully.")





### Command to display your current informational statistics
@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):

    namecheck = db.execute("SELECT * FROM kappaINFO WHERE username=?", (interaction.user.name,))
    row = namecheck.fetchone()

    if row is not None:

        user_id = row[1] 
        periodicals_response = ef.periodical_Requests(user_id)

        ## Get Soul Egg amount and convert to readable form
        total_soul = ef.numer_formatter(row[3])

        ## Embed discord text bubble
        embed = Embed(title="Egg Inc Profile",description="A amazingly amazing description of your current egg inc", color=0xffd700)  
        embed.add_field(name="Discord User", value=interaction.user.name, inline=False)
        embed.add_field(name="Egg Inc IGN", value=periodicals_response.backup.user_name, inline=False)                                   
        embed.add_field(name="Soul Eggs", value=total_soul, inline=False)
        embed.add_field(name="Prophecy Eggs", value=row[4], inline=False)
        embed.add_field(name="Earning Bonus", value=ef.numer_formatter(row[5]) + "%", inline=False)

        # ephemeral=True to hide
        await interaction.response.send_message(embed=embed, ephemeral=False)

    else:
        await interaction.response.send_message(f"The user {interaction.user.name} has not yet joined to be able to use this command.")





## Command to update your currently stored data to new data
@bot.tree.command(name="update")
async def update(interaction: discord.Interaction):

    namecheck = db.execute("SELECT * FROM kappaINFO WHERE username=?", (interaction.user.name,))
    row = namecheck.fetchone()

    if row is not None:

        user_id = row[1] 
        periodicals_response = ef.periodical_Requests(user_id)

        new_eb = ef.calc_earning_bonus(periodicals_response)
        new_eb_percent = ef.numer_formatter(new_eb)

        ## Get Soul Egg amount and convert to readable form
        old_soul = ef.numer_formatter(row[3])
        new_soul = ef.numer_formatter(periodicals_response.backup.game.soul_eggs_d)

        ## Embed discord text bubble
        embed = Embed(title="Egg Inc Profile",description="A amazingly amazing update of your current egg inc", color=0xffd700)  
        embed.add_field(name="Discord User", value=interaction.user.name, inline=False)
        embed.add_field(name="Egg Inc IGN", value=periodicals_response.backup.user_name, inline=False)  

        ##OLD INFO Embed              
        old_info = f"{old_soul}  {ef.se} \u2003 {row[4]}  {ef.pe} \u2003 {ef.numer_formatter(row[5])} {ef.eb}"              
        embed.add_field(name=ef.old, value= old_info, inline=False)

        ##NEW INFO Embed
        new_info = f"{new_soul}  {ef.se} \u2003 {periodicals_response.backup.game.eggs_of_prophecy}  {ef.pe} \u2003 {new_eb_percent} {ef.eb}" 
        embed.add_field(name=ef.new, value= new_info, inline=False)
        
        ##Update database with newly generated values
        db.execute("UPDATE kappaINFO SET soul_eggs=?, proph_eggs=?, earning_bonus=? WHERE username=?", (periodicals_response.backup.game.soul_eggs_d, periodicals_response.backup.game.eggs_of_prophecy, new_eb, interaction.user.name))
        db.commit()

        # ephemeral=True to hide
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    
    else:
        await interaction.response.send_message("Not currently registered in the database please register!")
    




### Command to view other users stats (nothing private like eid)
@bot.tree.command(name="spy")
@app_commands.describe(discord_user = "Enter Discord User TO Spy on")
async def spy(interaction: discord.Interaction, discord_user: str):

    namecheck = db.execute("SELECT * FROM kappaINFO WHERE username=?", (discord_user,))
    row = namecheck.fetchone()

    if row is not None:

        user_id = row[1] 
        periodicals_response = ef.periodical_Requests(user_id)

        ## Get Soul Egg amount and convert to readable form
        total_soul = ef.numer_formatter(row[3])

        ## Embed discord text bubble
        embed = Embed(title="Egg Inc Profile",description="A amazingly amazing description of your current egg inc", color=0xffd700)  
        embed.add_field(name="Discord User", value=discord_user, inline=False)
        embed.add_field(name="Egg Inc IGN", value=periodicals_response.backup.user_name, inline=False)                                   
        embed.add_field(name="Soul Eggs", value=total_soul, inline=False)
        embed.add_field(name="Prophecy Eggs", value=row[4], inline=False)
        embed.add_field(name="Earning Bonus", value=ef.numer_formatter(row[5]) + "%", inline=False)

        # ephemeral=True to hide
        await interaction.response.send_message(embed=embed, ephemeral=False)

    else:
        await interaction.response.send_message(f"{discord_user} does this person even exist???.")
    



## Command to Display leaderboard of current registered users Descending Order
@bot.tree.command(name="lb")
async def leader_board(interaction: discord.Interaction):
    list = db.execute("SELECT * FROM kappaINFO ORDER BY earning_bonus DESC")
    row =  list.fetchall()

    ## Header Points of Embed
    embed = Embed(title="Kappa Leaderboard",description="The board yes thats right THE BOARD", color=0xffd700)  
    embed.add_field(name="Rank", value="",inline=True)                                 
    embed.add_field(name="Egg Inc IGN", value="",inline=True)  
    embed.add_field(name="Earning Bonus", value="",inline=True)

    for idx,user in enumerate(row):

        ## Adding each player to list Descending Order
        embed.add_field(name="", value=idx+1,inline=True)                                 
        embed.add_field(name="", value=user[6],inline=True)  
        embed.add_field(name="", value=ef.numer_formatter(user[5]) + "%",inline=True)


    await interaction.response.send_message(embed=embed, ephemeral=False)



bot.run(TOKEN)

