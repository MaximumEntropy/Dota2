import urllib
import xml.etree.ElementTree as ET
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)
clf2 = svm.LinearSVC()
clf = svm.SVC()
logreg = linear_model.LogisticRegression(C=1e5)

apsched = BlockingScheduler()

API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

file_handler_match_id = open('match_ids.txt','r')
#file_handler_features = open('match_features.csv','a')
file_handler_features = open('match_features.csv','r')

#file_handler_features.writelines('Duration,tower_status_dire,tower_status_radiant,barracks_status_dire,barracks_status_radiant,radiant_win,first_blood_time,heroes')
#file_handler_features.writelines('\n')


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


	def get_match_details(self):
		match_url = MATCH_REQUEST_URL + self.match_id + '&key=' + API_KEY + '&format=XML'
		url_content = urllib.urlopen(match_url)
		url_content = url_content.read()
		self.parse_match(url_content)

	def parse_match(self,xml_content):
		root = ET.fromstring(xml_content)
		for child in root:
			if child.tag == 'duration':
				duration = int(child.text)
				if duration <= 1200:
					print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
					self.valid = False
					self.match_duration = duration
					file_handler_features.write(str(duration) + ',')
				else :
					print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
					self.match_duration = duration
					self.valid = True
					file_handler_features.write(str(duration) + ',')
			elif child.tag == 'tower_status_dire':
				self.tower_status_dire = int(child.text)
				file_handler_features.write(str(child.text) + ',')
			elif child.tag == 'tower_status_radiant':
				self.tower_status_radiant = int(child.text)
				file_handler_features.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_dire':
				self.barracks_status_dire = int(child.text)
				file_handler_features.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_radiant':
				self.barracks_status_radiant = int(child.text)
				file_handler_features.write(str(child.text) + ',')
			elif child.tag == 'radiant_win':
				if child.text == 'true':
					self.match_winner = 1
					file_handler_features.write(str(1) + ',')
				else:
					self.match_winner = 0
					file_handler_features.write(str(0) + ',')
			elif child.tag == 'first_blood_time':
				self.first_blood_time = int(child.text)
				file_handler_features.write(str(child.text) + ',')
			for child1 in child:
				for player in child1:
					if player.tag == 'hero_id':
						self.radiant_heroes.append(int(player.text))
						file_handler_features.write(str(player.text) + ',')


def fetch_match_ids():
	match_ids = file_handler_match_id.readlines()
	match_ids = list(set(match_ids))
	return match_ids

def populate_match_details():
	match_ids = fetch_match_ids()
	print match_ids
	matches = []
	match_ids = match_ids[6550:]
	match_counter = 6500
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
		file_handler_features.write('\n')
		match_counter = match_counter + 1
	return matches

def construct_training_data(match_data):
	training_data = []
	results = []
	for match in match_data:
		if match.valid == False:
			continue
		radiant_heroes = match.radiant_heroes
		feature_vector = [0 for i in range(220)]
		for hero in radiant_heroes[:5]:
			feature_vector[hero] = 1
		for hero in radiant_heroes[5:]:
			feature_vector[hero+110] = 1
		training_data.append(feature_vector)
		winner = match.match_winner
		results.append(winner)
	return training_data,results


def leave_one_out(training_data,test_point,results,test_result):
	rf.fit(training_data,results)
	result = rf.predict(test_point)
	if result == test_result:
		return True
	else:
		return False

def temp_classifier():
	x = file_handler_features.readlines()
	training_data = []
	results = []
	del x[0]
	for line in x:
		line = line.strip()
		line = line.split(',')
		#print line
		item = line[:10]
		duration = int(line[11])
		if duration < 1200 or len(line) >= 20:
			continue
		item = [int(item[i]) for i in range(len(item))]
		feature_vector = [0 for i in range(221)]
		for hero in item[:5]:
			feature_vector[hero] = 1
		for hero in item[5:]:
			feature_vector[hero+110] = 1
		training_data.append(feature_vector)
		results.append(int(line[10]))
	correct = 0
	wrong = 0
	for i in range(len(training_data)):
		print 'Iteration : ' + str(i)
		test_point = training_data[i]
		test_result = results[i]
		remaining_training = [training_data[j] for j in range(len(training_data)) if i!=j]
		remaining_results = [results[j] for j in range(len(results)) if i!=j]
		result = leave_one_out(remaining_training,test_point,remaining_results,test_result)
		if result == True:
			print 'True'
			correct = correct + 1
		else:
			print 'False'
			wrong = wrong + 1
		accuracy = (float(correct))/(float(correct) + float(wrong))
		print 'Accuracy : ' + str(accuracy)
	'''
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	rf.fit(training_data,results_training)
	correct = 0
	wrong = 0
	for i in range(len(test_data)):
		result = rf.predict(test_data[i])
		if result == results_test[i]:
			correct = correct + 1
			print 'Correct : ' + str(result)
		else:
			wrong  = wrong + 1
			print 'Wrong : ' + str(result)
	print correct,wrong
	accuracy = (float(correct))/(float(correct) + float(wrong))
	print 'Accuracy : ' + str(accuracy)
	'''

def classifier(training_data,results):
	test_data = training_data[-50:]
	training_data = training_data[:-50]
	test_results = results[-50:]
	results = results[-50:]
	print 'Fitting data ... '
	clf.fit(training_data,results)
	correct = 0
	wrong = 0
	print 'Clasifying data ... '
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


'''
x = populate_match_details()
training_data,results = construct_training_data(x)
classifier(training_data,results)
'''

temp_classifier()



