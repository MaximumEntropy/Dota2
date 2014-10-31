import xml.etree.ElementTree as ET

API_KEY = '13B0BA67AC391D42DF8CE47B65AE87FB'

GAMES_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key='

MATCH_REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='

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


def parse_match(xml_content,match_object):
	root = ET.fromstring(xml_content)
	for child in root:
		if child.tag == 'duration':
			duration = int(child.text)
			if duration <= 1200:
				print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
				match_object.valid = False
				match_object.match_duration = duration
				file_handler_features_heroes.write(str(duration) + ',')
			else :
				print 'Match Took : ' + str(float(duration)/60) + ' Minutes'
				match_object.match_duration = duration
				match_object.valid = True
				file_handler_features_heroes.write(str(duration) + ',')
		elif child.tag == 'tower_status_dire':
			match_object.tower_status_dire = int(child.text)
			file_handler_features_heroes.write(str(child.text) + ',')
		elif child.tag == 'tower_status_radiant':
			match_object.tower_status_radiant = int(child.text)
			file_handler_features_heroes.write(str(child.text) + ',')
		elif child.tag == 'barracks_status_dire':
			match_object.barracks_status_dire = int(child.text)
			file_handler_features_heroes.write(str(child.text) + ',')
		elif child.tag == 'barracks_status_radiant':
			match_object.barracks_status_radiant = int(child.text)
			file_handler_features_heroes.write(str(child.text) + ',')
		elif child.tag == 'radiant_win':
			if child.text == 'true':
				match_object.match_winner = 1
				file_handler_features_heroes.write(str(1) + ',')
			else:
				match_object.match_winner = 0
				file_handler_features_heroes.write(str(0) + ',')
		elif child.tag == 'first_blood_time':
			match_object.first_blood_time = int(child.text)
			file_handler_features_heroes.write(str(child.text) + ',')
		for child1 in child:
			curr_hero_stuff = []
			for player in child1:
				if player.tag == 'hero_id':
					#match_object.radiant_heroes.append(int(player.text))
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
			match_object.radiant_heroes.append(curr_hero_stuff)
	return match_object