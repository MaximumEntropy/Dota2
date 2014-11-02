import xml_parser
import urllib
import xml.etree.ElementTree as ET

file_handler_match_id = open('match_ids.txt','r')
#file_handler_features = open('match_features.csv','a')
file_handler_features = open('match_features.csv','r')

file_handler_features_heroes = open('match_features_heroes.csv','a')

API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

Match_objects = []

class Match():

	'''
	Constructor Function initializing all items of the class. Just to get an idea what parameters we want to be using
	'''

	def __init__(self):
		self.match_duration = 0 # Duration of the match in seconds.
		self.match_winner = 0 # 1 if Radiant Victory or 0 if Dire Victory.
		self.radiant_heroes = [] # Dictionary of hero vs characteristics (GPM,XPM,KDA) Single Metric?  
		self.tower_status_radiant = 0
		self.tower_status_dire = 0
		self.barracks_status_radiant = 0
		self.barracks_status_dire = 0
		self.match_id = 0
		self.first_blood_time = 0
		self.valid = True


	def get_match_details(self,file_handler_features_heroes):
		match_url = MATCH_REQUEST_URL + self.match_id + '&key=' + API_KEY + '&format=XML'
		url_content = urllib.urlopen(match_url)
		url_content = url_content.read()
		self.parse_match(url_content,file_handler_features_heroes)


	def parse_match(self,xml_content,file_handler_features_heroes):
		root = ET.fromstring(xml_content)
		for child in root:
			if child.tag == 'duration':
				duration = int(child.text)
				if duration <= 1200:
					print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
					self.valid = False
					self.match_duration = duration
					file_handler_features_heroes.write(str(duration) + ',')
				else :
					print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
					self.match_duration = duration
					self.valid = True
					file_handler_features_heroes.write(str(duration) + ',')
			elif child.tag == 'tower_status_dire':
				self.tower_status_dire = int(child.text)
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'tower_status_radiant':
				self.tower_status_radiant = int(child.text)
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_dire':
				self.barracks_status_dire = int(child.text)
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_radiant':
				self.barracks_status_radiant = int(child.text)
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'radiant_win':
				if child.text == 'true':
					self.match_winner = 1
					file_handler_features_heroes.write(str(1) + ',')
				else:
					self.match_winner = 0
					file_handler_features_heroes.write(str(0) + ',')
			elif child.tag == 'first_blood_time':
				self.first_blood_time = int(child.text)
				file_handler_features_heroes.write(str(child.text) + ',')
			for child1 in child:
				curr_hero_stuff = []
				for player in child1:
					if player.tag == 'hero_id':
						#self.radiant_heroes.append(int(player.text))
						file_handler_features_heroes.write(str(player.text) + ',')
						curr_hero_stuff.append(player.text)
					if player.tag == 'kills':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'deaths':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'assists':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'gold_per_min':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'xp_per_min':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'level':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'hero_damage':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'assists':
						curr_hero_stuff.append(player.text)
						file_handler_features_heroes.write(str(player.text) + ',')
				self.radiant_heroes.append(curr_hero_stuff)

def get_match_recursively(file_handler_match_id,file_handler_features_heroes):
	match_list_url = GAMES_REQUEST_URL + API_KEY + '&skill=3'
	url_content = urllib.urlopen(match_list_url)
	url_buffer = url_content.read()
	match_ids,last_match = xml_parser.parse_match_list(url_buffer,file_handler_features_heroes)
	for match_id in match_ids:
		file_handler_match_id.write(str(match_id) + '\n')
	for i in range(10000):
		print 'Iteration Number : ' + str(i)
		match_list_url = GAMES_REQUEST_URL + API_KEY + '&start_at_match_id=' + str(last_match) + '&skill=3'
		url_content = urllib.urlopen(match_list_url)
		url_buffer = url_content.read()
		match_ids,last_match = xml_parser.parse_match_list(url_buffer)
		print match_ids,len(match_ids)
		for match_id in match_ids:
			file_handler_match_id.write(str(match_id) + '\n')
		if last_match == '':
			return

def fetch_match_ids(file_handler_match_id):
	match_ids = file_handler_match_id.readlines()
	match_ids = list(set(match_ids))
	return match_ids

def populate_match_details(file_handler_match_id):
	match_ids = fetch_match_ids(file_handler_match_id)
	print match_ids
	matches = []
	print len(match_ids)
	print match_ids[7908]
	match_ids = match_ids[7908:]
	match_counter = 7908
	for match_id in match_ids:
		print 'Parsing match : ' + str(match_counter)
		temp_match = Match()
		temp_match.match_id = match_id
		temp_match.get_match_details()
		matches.append(temp_match)
		print 'Match Details ... '
		print 'Duration : ' + str(temp_match.match_duration)
		print 'winner : ' + str(temp_match.match_winner)
		print 'Radiant Heroes : ' + str(temp_match.radiant_heroes)
		print 'first_blood_time : ' + str(temp_match.first_blood_time)
		print 'barracks_status_radiant : ' + str(temp_match.barracks_status_radiant)
		print 'barracks_status_dire	: ' + str(temp_match.barracks_status_dire)
		print 'tower_status_radiant : ' + str(temp_match.tower_status_radiant)
		print 'tower_status_dire : ' + str(temp_match.tower_status_dire)
		file_handler_features_heroes.write('\n')
		match_counter = match_counter + 1
	return matches