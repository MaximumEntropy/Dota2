import xml.etree.ElementTree as ET
import os
file_handler_features_heroes = open('features_local.csv','w')
match_number = 1
for file_name in os.listdir('Matches'):
	print 'Match Number : ' + str(match_number)
	if file_name[-3:] == 'xml':
		try:
			tree = ET.parse('Matches/'+file_name)
		except ET.ParseError:
			print 'Parse Failed!!'
			continue
		root = tree.getroot()
		for child in root:
			if child.tag == 'duration':
				duration = int(child.text)
				file_handler_features_heroes.write(str(duration) + ',')
			elif child.tag == 'tower_status_dire':
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'tower_status_radiant':
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_dire':
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'barracks_status_radiant':
				file_handler_features_heroes.write(str(child.text) + ',')
			elif child.tag == 'radiant_win':
				if child.text == 'true':
					file_handler_features_heroes.write(str(1) + ',')
				elif child.text == 'false':
					file_handler_features_heroes.write(str(0) + ',')
			elif child.tag == 'first_blood_time':
				file_handler_features_heroes.write(str(child.text) + ',')
			for child1 in child:
				curr_hero_stuff = []
				for player in child1:
					if player.tag == 'hero_id':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'kills':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'deaths':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'assists':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'gold_per_min':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'xp_per_min':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'level':
						file_handler_features_heroes.write(str(player.text) + ',')
					if player.tag == 'hero_damage':
						file_handler_features_heroes.write(str(player.text) + ',')
		match_number = match_number + 1
		file_handler_features_heroes.write('\n')

