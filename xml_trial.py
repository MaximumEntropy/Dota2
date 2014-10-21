import urllib
import xml.etree.ElementTree as ET
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn import svm

clf = svm.SVC(kernel='linear')

apsched = BlockingScheduler()

API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

file_handler_match_id = open('match_ids.txt','ab+')
file_handlier_features = open('match_features.txt','w')

class Match():

	'''
	Constructor Function initializing all items of the class. Just to get an idea what parameters we want to be using
	'''

	def __init__(self):
		match_duration = 0 # Duration of the match in seconds.
		match_winner = 0 # 1 if Radiant Victory or 0 if Dire Victory.
		radiant_heroes = [] # Dictionary of hero vs characteristics (GPM,XPM,KDA) Single Metric?  
		dire_heroes = []
		tower_status_radiant = 0
		tower_status_dire = 0
		barracks_status_radiant = 0
		barracks_status_dire = 0
		match_id = 0
		first_blood_time = 0
		valid = True


	def get_match_details(self):
		match_ids = 
		match_url = MATCH_REQUEST_URL + self.match_id + '&key=' + API_KEY + '&format=XML'
		url_content = urllib.urlopen(match_url)
		self.parse_match(url_content)

	def parse_match(self,xml_content):
		root = ET.fromstring(xml_content)
		for child in root:
			if child.tag == 'duration':
				duration = int(child.text)
				if duration <= 1200:
					self.valid = False
				else :
					self.match_duration = duration
			elif child.tag == 'tower_status_dire':
				self.tower_status_dire = int(child.text)
			elif child.tag == 'tower_status_radiant':
				self.tower_status_radiant = int(child.text)
			elif child.tag == 'barracks_status_dire':
				self.barracks_status_dire = int(child.text)
			elif child.tag == 'barracks_status_radiant':
				self.barracks_status_radiant = int(child.text)
			elif child.tag == 'radiant_win':
				self.match_winner = int(child.text)
			elif child.tag == 'first_blood_time':
				self.first_blood_time = int(child.text)
			for child1 in child:
				counter = 1
				for player in child1:
					if player.tag == 'hero_id':
						if counter <=5:
							self.radiant_heroes.append(int(player.text))
						else:
							self.dire_heroes.append(int(player.text))

def fetch_match_ids():
	match_ids = file_handler_match_id.readlines()
	match_ids = list(set(match_ids))
	return match_ids

def populate_match_details():
	match_ids = fetch_match_ids()
	matches = []
	for match_id in match_ids:
		temp_match = Match()
		temp_match.match_id = match_id
		temp_match.get_match_details()
		matches.append(temp_match)
	return matches

def construct_training_data(match_data):
	training_data = []
	results = []
	for match in matches:
		if match.valid == False:
			continue
		radiant_heroes = match.radiant_heroes
		dire_heroes = match.dire_heroes
		feature_vector = [0 for i in range(220)]
		for hero in radiant_heroes:
			feature_vector[hero] = 1
		for hero in dire_heroes:
			temp_vector[hero+110] = 1
		training_data.append(feature_vector)
		winner = match.match_winner
		results.append(winner)
	return training_data,results

def classifier(training_data,results):
	test_data = training_data[-50:]
	training_data = training_data[:-50]
	test_results = results[-50:]
	results = results[-50:]
	clf.fit(training_data,results)
	correct = 0
	wrong = 0
	for i in range(len(test_data)):
		result = clf.predict(test_data[i])
		if result == test_results[i]:
			correct = correct + 1
		else:
			wrong  = wrong + 1
	accuracy = (float(correct))/float(correct) + float(wrong)
	print 'Accuracy : ' + str(accuracy)

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
	try:
		return match_ids,curr_id
	except UnboundLocalError:
		return match_ids, ''

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
		if last_match == '':
			return

'''
A = Match()
A.match_id = '27110133'
A.get_match_details()
'''
#get_match_recursively()
#apsched.add_job(get_match_recursively, trigger='interval', seconds=1800)
#apsched.start() # will block


x = populate_match_details()
training_data,results = construct_training_data(x)




