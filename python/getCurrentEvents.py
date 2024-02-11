import requests
import ei_pb2
import base64

user_id = 'EI4579467126636544'

periodicals_request = ei_pb2.EggIncFirstContactRequest()
periodicals_request.ei_user_id = user_id
periodicals_request.client_version = 42

url = 'https://www.auxbrain.com/ei/bot_first_contact' 
data = { 'data' : base64.b64encode(periodicals_request.SerializeToString()).decode('utf-8') }
response = requests.post(url, data = data)

periodicals_response = ei_pb2.EggIncFirstContactResponse()
periodicals_response.ParseFromString(base64.b64decode(response.text))

print(periodicals_response.backup.game.new_player_event_end_time)