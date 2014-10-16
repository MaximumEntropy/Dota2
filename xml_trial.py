import urllib
API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

class Match():

	'''
	Constructor Function initializing all items of the class. Just to get an idea what parameters we want to be using
	'''

	def __init__(self):
		match_duration = 0 # Duration of the match in seconds.
		match_winner = 0 # 0 if Radiant Victory or 1 if Dire Victory.
		radiant_heroes = {} # Dictionary of hero vs characteristics (GPM,XPM,KDA) Single Metric?  
		dire_heroes = {} 
		tower_status_radiant = 0
		tower_status_dire = 0
		barracks_status_radiant = 0
		barracks_status_dire = 0
		match_id = 0


	def get_match_details(self):
		match_url = MATCH_REQUEST_URL + self.match_id + '&key=' + API_KEY
		url_content = urllib.urlopen(match_url)
		print url_content.read()


'''
Recursively get matches using the WebAPI
'''

Match_objects = []

def parse_match_list(xml_content):
	

def get_match_recursively():
	for i in range(10):
		match_list_url = GAMES_REQUEST_URL + API_KEY
		url_content = urllib.urlopen(match_list_url)
		url_buffer = url_content.read()
		parse_match_list(url_buffer)


A = Match()
A.match_id = '27110133'
A.get_match_details()