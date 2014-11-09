file_handler_feature_vectors = open('feature_vectors.csv','w')
file_handler_feature_vectors_heroes = open('feature_vectors_heroes.csv','w')
file_handler_feature_vectors_reverse = open('feature_vectors_reverse.csv','w')
file_handler_feature_vectors_heroes_reverse = open('feature_vectors_heroes_reverse.csv','w')
file_handler_xml_extracted = open('features_local.csv','r')
file_handler_regression_features = open('features_regression.csv','w')
lines = file_handler_xml_extracted.readlines()
lines = list(set(lines))
def populate_regression_features():
	for line in lines:
		line = line.strip()
		line = line.split(',')
		del line[-1]
		line = [int(z) for z in line]
		hero_data = line[:80]
		hero_data=[hero_data[x:x+8] for x in xrange(0, len(hero_data), 8)]
		hero_ids = [temp[0] for temp in hero_data]
		if len(hero_data) < 10:
			continue
		result = int(line[80])
		if result == 0:
			result = -1
		duration = int(line[81])
		if duration < 1200:
			continue
		all_kills = [temp[1] for temp in hero_data]
		radiant = all_kills[:5]
		dire = all_kills[5:]
		diff_kills = abs(sum(radiant)-sum(dire))
		all_assists = [temp[3] for temp in hero_data]
		radiant = all_assists[:5]
		dire = all_assists[5:]
		diff_assists = abs(sum(radiant)-sum(dire))
		all_gpm = [temp[4] for temp in hero_data]
		radiant = all_gpm[:5]
		dire = all_gpm[5:]
		diff_gpm = abs(sum(radiant)-sum(dire))
		all_xpm = [temp[5] for temp in hero_data]
		radiant = all_xpm[:5]
		dire = all_xpm[5:]
		diff_xpm = abs(sum(radiant)-sum(dire))
		all_levels = [temp[7] for temp in hero_data]
		radiant = all_levels[:5]
		dire = all_levels[5:]
		diff_levels = abs(sum(radiant)-sum(dire))
		print diff_kills,diff_assists,diff_gpm,diff_xpm,diff_levels
		margin = float(diff_kills) + float(diff_assists)/2.0 + float(diff_gpm)/100 + float(diff_xpm)/100 + float(diff_levels) + (1.0/duration) * 100000
		margin = margin * result
		feature_vector = [0 for i in range(221)]
		for hero in hero_ids[:5]:
			feature_vector[int(hero)] = 1
		for hero in hero_ids[5:]:
			feature_vector[int(hero)+110] = 1
		feature_vector.append(margin)
		for item in feature_vector:
			file_handler_regression_features.write(str(item) + ',')
		file_handler_regression_features.write('\n')


def populate_hero_stats(feature_content):
	hero_dict = {}
	for line in feature_content:
		line = line.strip()
		line = line.split(',')
		if len(line) > 90:
			continue
		hero_data = line[:80]
		hero_data=[hero_data[x:x+8] for x in xrange(0, len(hero_data), 8)]
		if len(hero_data) < 10:
			continue
		for hero in hero_data:
			hero_id = hero[0]
			if hero_id not in hero_dict:
				hero_dict[hero_id] = []
			kills = hero[1]
			deaths = hero[2]
			assists = hero[3]
			gpm = hero[4]
			xpm = hero[5]
			hero_damage = hero[6]
			level = hero[7]
			feature = float(kills) - float(deaths) + (float(assists)/2) + float(level) + float(gpm)/100 + float(xpm)/100 + float(hero_damage)/10000 
			hero_dict[hero_id].append(feature)
	for hero in hero_dict:
		hero_dict[hero] = float(float(sum(hero_dict[hero]))/len(hero_dict[hero]))
	return hero_dict

hero_dict = populate_hero_stats(lines)
match_counter = 1
for line in lines:
	print 'Match Counter : ' + str(match_counter)
	line = line.strip()
	line = line.split(',')
	hero_data = line[:80]
	hero_data=[hero_data[x:x+8] for x in xrange(0, len(hero_data), 8)]
	hero_ids = [temp[0] for temp in hero_data]
	if len(hero_data) < 10:
		continue
	result = int(line[80])
	duration = int(line[81])
	if int(duration) < 1200:
		continue
	feature_vector = [0 for i in range(221)]
	feature_vector_reverse = [0 for i in range(221)]
	for hero in hero_ids[:5]:
		feature_vector[int(hero)] = 1
	for hero in hero_ids[5:]:
		feature_vector[int(hero)+110] = 1

	for hero in hero_ids[5:]:
		feature_vector_reverse[int(hero)] = 1
	for hero in hero_ids[:5]:
		feature_vector_reverse[int(hero)+110] = 1
	
	feature_vector.append(str(result))
	print result
	if result == 1:
		inv_result = 0
	else:
		inv_result = 1
	feature_vector_reverse.append(str(inv_result))

	for item in feature_vector:
		file_handler_feature_vectors.write(str(item) + ',')
	file_handler_feature_vectors.write('\n')

	for item in feature_vector_reverse:
		file_handler_feature_vectors_reverse.write(str(item) + ',')
	file_handler_feature_vectors_reverse.write('\n')

	feature_vector = [0 for i in range(231)]
	feature_vector_reverse = [0 for i in range(231)]
	counter = 0
	for hero in hero_ids[:5]:
		feature_vector[int(hero)] = 1
		feature_vector[221+counter] = hero_dict[hero]/float(50)
		counter = counter + 1
	for hero in hero_ids[5:]:
		feature_vector[int(hero)+110] = 1
		feature_vector[221+counter] = hero_dict[hero]/float(50)
		counter = counter + 1

	counter = 0
	for hero in hero_ids[5:]:
		feature_vector_reverse[int(hero)] = 1
		feature_vector_reverse[221+counter] = hero_dict[hero]/float(50)
		counter = counter + 1
	for hero in hero_ids[:5]:
		feature_vector_reverse[int(hero)+110] = 1
		feature_vector_reverse[221+counter] = hero_dict[hero]/float(50)
		counter = counter + 1

	feature_vector.append(str(result))
	feature_vector_reverse.append(str(inv_result))

	for item in feature_vector:
		file_handler_feature_vectors_heroes.write(str(item) + ',')
	file_handler_feature_vectors_heroes.write('\n')

	for item in feature_vector_reverse:
		file_handler_feature_vectors_heroes_reverse.write(str(item) + ',')
	file_handler_feature_vectors_heroes_reverse.write('\n')
	
	match_counter = match_counter + 1


populate_regression_features()





