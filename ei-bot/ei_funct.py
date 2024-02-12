#==================================================================#
############### Bot Created By: Taijitu (rankopolat) ###############
### Repository: https://github.com/rankopolat/EggInc-Discord-Bot ###
#==================================================================#

#ei imports
import requests
import ei_pb2
import base64


## Creating Globals to Access through folder
global old,new,se,pe,eb
old = ":regional_indicator_o: :regional_indicator_l: :regional_indicator_d:" 
new = ":regional_indicator_n: :regional_indicator_e: :regional_indicator_w:"  
se = "<:Egg_soul:1206562020342628392>"
pe = "<:Egg_of_Prophecy:1206564103963807765>"
eb = ":chart_with_upwards_trend:"



### For earning bonus and soul egg ease of reading
def numer_formatter(number):

    format_souls_eggs = '{:_.0f}'.format(number)

    suffixes = {

        1_000: 'K',      # Thousand
        1_000_000: 'M',     # Million
        1_000_000_000: 'B',    # Billion
        1_000_000_000_000: 'T',    # Trillion
        1_000_000_000_000_000: 'q',   # Quadrillion
        1_000_000_000_000_000_000: 'Q',   # Quintillion
        1_000_000_000_000_000_000_000: 's',   # Sextillion
        1_000_000_000_000_000_000_000_000: 'S',   # Septillion
        1_000_000_000_000_000_000_000_000_000: 'O',   # Octillion
        1_000_000_000_000_000_000_000_000_000_000: 'N',   # Nonillion
        1_000_000_000_000_000_000_000_000_000_000_000: 'D'   # Decillion

    }

    for divisor, suffix in sorted(suffixes.items(), reverse=True):
        if number >= divisor:
            return f"{number / divisor:,.3f}{suffix}"
    
    return str(number)





### Periodical Requests accessing url:bot_first_contract
def periodical_Requests(user_id):

    periodicals_request = ei_pb2.EggIncFirstContactRequest()
    periodicals_request.ei_user_id = user_id
    periodicals_request.client_version = 42

    url = 'https://www.auxbrain.com/ei/bot_first_contact' 
    data = { 'data' : base64.b64encode(periodicals_request.SerializeToString()).decode('utf-8') }
    response = requests.post(url, data = data)

    periodicals_response = ei_pb2.EggIncFirstContactResponse()
    periodicals_response.ParseFromString(base64.b64decode(response.text))


    return periodicals_response




### Maths To calculate Earnings bonus
def calc_earning_bonus(periodicals_response):

    prophecy_bonus = periodicals_response.backup.game.epic_research[21].level
    soul_bonus = periodicals_response.backup.game.epic_research[15].level
    new_proph = periodicals_response.backup.game.eggs_of_prophecy
    

    #Individual earning bonus the (eb) per soul egg
    #(1.05 + 0.01 * amount of epic research (prophecybonus)) ** total prophecy eggs * (10 + amount of epic research (soul egg bonus))
    indi_eb = (1.05 + 0.01 * prophecy_bonus) ** new_proph * (10 + soul_bonus)
    total_eb = indi_eb * periodicals_response.backup.game.soul_eggs_d

    return total_eb



### Create initial database table aswell as alternations / updates to main table
def create_table(db):
    
    cur = db.cursor()
    #Table Creation
    cur.execute('''
    CREATE TABLE IF NOT EXISTS kappaINFO (
        id integer PRIMARY KEY AUTOINCREMENT,
        eid text NOT NULL,
        username text NOT NULL,
        soul_eggs REAL NOT NULL,
        proph_eggs INTEGER NOT NULL,
        earning_bonus REAL NOT NULL,
        ei_ign text NOT NULL
        )
    ''')


    #data = cur.execute("SELECT * FROM kappaINFO")


    ### Left For Updates or ALTERNATION within the table without losing data
    '''for row in data:
        
        pr = periodical_Requests(row[1])

        db.execute("UPDATE kappaINFO SET ei_ign=? WHERE username=?", (pr.backup.user_name, row[2]))
        print(pr.backup.user_name)

    print()
    for row in data:
        print(row)'''

    db.commit()


