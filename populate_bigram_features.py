import itertools
f = open('features_local.csv','r')
file_handler_feature_vectors = open('bigram_features.csv','w')
lines = f.readlines()
hero_ids = range(111)
hero_bigrams = itertools.combinations(hero_ids,2)
bigram_dict = {}
counter = 1
for bigram in hero_bigrams:
	bigram_dict[bigram] = counter
	counter = counter + 1

counter = 1
for line in lines:
	print 'Line Number : ' + str(counter)
	print line
	line = line.strip()
	line = line.split(',')
	hero_data = line[:80]
	hero_data=[hero_data[x:x+8] for x in xrange(0, len(hero_data), 8)]
	hero_ids = [temp[0] for temp in hero_data]
	if len(line) < 80:
		continue
	hero_ids = [int(x) for x in hero_ids]
	if len(hero_data) < 10:
		continue
	result = int(line[80])
	duration = int(line[81])
	if int(duration) < 1200:
		continue
	game_bigrams_radiant = itertools.combinations(list(set(hero_ids[:5])),2)
	game_bigrams_dire = itertools.combinations(list(set(hero_ids[5:])),2)
	feature_vector = [0 for i in range(6105*2+1)]
	for bigram in game_bigrams_radiant:
		try:
			bigram_id = bigram_dict[bigram]
		except KeyError:
			bigram = bigram[::-1]
			bigram_id = bigram_dict[bigram]
		feature_vector[bigram_id] = 1
	for bigram in game_bigrams_dire:
		try:
			bigram_id = bigram_dict[bigram]
		except KeyError:
			bigram = bigram[::-1]
			bigram_id = bigram_dict[bigram]
		feature_vector[6105 + bigram_id] = 1
	feature_vector.append(str(result))
	for item in feature_vector:
		file_handler_feature_vectors.write(str(item) + ',')
	file_handler_feature_vectors.write('\n')
	counter = counter + 1