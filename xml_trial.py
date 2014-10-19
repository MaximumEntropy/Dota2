import urllib
import xml.etree.ElementTree as ET

API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

file_handler_match_id = open('match_ids.txt','a')

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
	match_ids = []
	root = ET.fromstring(xml_content)
	for child in root:
		if child.tag == 'matches':
			for child1 in child:
				for child2 in child1:
					if child2.tag == 'match_id':
						curr_id = child2.text
					if child2.tag == 'lobby_type':
						lobby_type = child2.text
						if int(lobby_type) in [7,2]:
							match_ids.append(curr_id)
	return match_ids,curr_id

def get_match_recursively():
	match_list_url = GAMES_REQUEST_URL + API_KEY + '&skill=3'
	url_content = urllib.urlopen(match_list_url)
	url_buffer = url_content.read()
	match_ids,last_match = parse_match_list(url_buffer)
	for match_id in match_ids:
		file_handler_match_id.write(str(match_id) + '\n')
	for i in range(10000):
		print 'Iteration Number : ' + str(i)
		match_list_url = GAMES_REQUEST_URL + API_KEY + '&start_at_match_id=' + str(last_match) + '&skill=3'
		url_content = urllib.urlopen(match_list_url)
		url_buffer = url_content.read()
		match_ids,last_match = parse_match_list(url_buffer)
		print match_ids,len(match_ids)
		for match_id in match_ids:
			file_handler_match_id.write(str(match_id) + '\n')


'''
A = Match()
A.match_id = '27110133'
A.get_match_details()
'''
get_match_recursively()