import operator
import itertools
g = open('results.txt','w')
def populate_hero_stats(feature_content):
	num_matches = 0
	hero_dict = {}
	hero_dict_count = {}
	hero_dict_bigram = {}
	hero_dict_winrate = {}
	for item in itertools.permutations(range(110),2):
		hero_dict_bigram[item] = 0
	#print hero_dict_bigram
	for line in feature_content:
		line = line.strip()
		line = line.split(',')
		if len(line) > 90:
			continue
		hero_data = line[:80]
		hero_data=[hero_data[x:x+8] for x in xrange(0, len(hero_data), 8)]
		if len(hero_data) < 10:
			continue
		num_matches = num_matches + 1
		hero_ids = [int(i[0]) for i in hero_data]
		hero_bigrams = itertools.permutations(hero_ids,2)
		for bigram in hero_bigrams:
			try:
				hero_dict_bigram[bigram] = hero_dict_bigram[bigram] + 1
			except KeyError:
				pass
		for hero in hero_data:
			hero_id = hero[0]
			if hero_id not in hero_dict:
				hero_dict[hero_id] = []
			if hero_id not in hero_dict_count:
				hero_dict_count[hero_id] = 0
			hero_dict_count[hero_id] = hero_dict_count[hero_id] + 1
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
	sorted_x = sorted(hero_dict_count.items(), key=operator.itemgetter(1))
	sorted_y = sorted(hero_dict_bigram.items(), key=operator.itemgetter(1))
	#print sorted_x
	#print hero_dict_bigram
	temp = []
	for item in sorted_x:
		picks = item[1]
		picks = float(picks)/float(num_matches)
		temp.append([item[0],picks])
	#print temp
	temp = []
	#print sorted_y
	print hero_dict_bigram[(73, 58)]
	print hero_dict_bigram[(43, 16)]
	print hero_dict_bigram[(75, 13)]
	for item in sorted_y:
		picks = item[1]
		picks = float(picks)/float(num_matches)
		temp.append([item[0],picks])
	g.write(str(temp))

f = open('features_local.csv','r')
x = f.readlines()
populate_hero_stats(x)