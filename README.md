# EggInc Discord Bot

This is a Discord Bot to monitor you and your friends Soul Eggs, Prophecy Eggs, earning bonus, leaderboard, contracts and all egg inc api related material
This is a query to the Egg Inc API made by refering the code https://github.com/derekantrican/EggIncAPI to get the protobuf and endpoints.

## Usage
To Use this Discord bot simply Clone the repo, cd to the python folder,
create a .ev file and add your discord token in the format DISCORD_TOKEN = ''
invite the bot to your server
and than run python bot.py (you may need to pip install a couple things like protobuf unless you already have it). 

## Commands
When you first invite the bot you need to join using

/join eid#
This will register you into the sqllite database so you nolonger need to register again

![image](https://github.com/rankopolat/EggInc-Discord-Bot/assets/116534934/1d3942ee-ddd7-414b-9329-75a27c805e9f)


/info
This command gives you a current info card on your statistics

![image](https://github.com/rankopolat/EggInc-Discord-Bot/assets/116534934/3dc586fe-fb7c-4f21-a1da-9d00d521b961)


/update
This command will update your eb, soul eggs, and prophecy eggs 

![image](https://github.com/rankopolat/EggInc-Discord-Bot/assets/116534934/a1b2dca8-f69a-44b7-92f8-e6a61d6be3e8)


/spy
This Command allows you to check other users statistics based from there discord username

![image](https://github.com/rankopolat/EggInc-Discord-Bot/assets/116534934/fe7dfe6a-8113-4063-ae7a-8ef9fe7b193b)



/lb
This Command creates a leaderboard of the users stored in the db based on eb% in descending order

![image](https://github.com/rankopolat/EggInc-Discord-Bot/assets/116534934/ce0ef319-2b35-42ef-af92-51f8d8d095a6)


