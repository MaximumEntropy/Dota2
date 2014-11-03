file_handler_feature_vectors = open('feature_vectors.csv','w')
file_handler_feature_vectors_heroes = open('feature_vectors_heroes.csv','w')
file_handler_xml_extracted = open('features_local.csv','r')
lines = file_handler_xml_extracted.readlines()
lines = list(set(lines))
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
	for hero in hero_ids[:5]:
		feature_vector[int(hero)] = 1
	for hero in hero_ids[5:]:
		feature_vector[int(hero)+110] = 1
	feature_vector.append(str(result))
	for item in feature_vector:
		file_handler_feature_vectors.write(str(item) + ',')
	file_handler_feature_vectors.write('\n')
	feature_vector = [0 for i in range(231)]
	counter = 0
	for hero in hero_ids[:5]:
		feature_vector[int(hero)] = 1
		feature_vector[221+counter] = hero_dict[hero]
		counter = counter + 1
	for hero in hero_ids[5:]:
		feature_vector[int(hero)+110] = 1
		feature_vector[221+counter] = hero_dict[hero]
		counter = counter + 1
	feature_vector.append(str(result))
	for item in feature_vector:
		file_handler_feature_vectors_heroes.write(str(item) + ',')

	file_handler_feature_vectors_heroes.write('\n')
	match_counter = match_counter + 1





