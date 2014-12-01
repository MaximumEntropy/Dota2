file_handler_features = open('features_local.csv','r')
lines = file_handler_features.readlines()
lines = list(set(lines))
training = lines[:-2000]
test = lines[-2000:]

def find_probability(hero_id_list,training):
	win_count = 0
	loss_count = 0 
	for line in training:
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
		hero_ids = set(hero_ids[:5])
		hero_id_list = set(hero_id_list)
		if hero_id_list.issubset(hero_ids):
			if result == 1:
				win_count = win_count + 1
			else:
				loss_count = loss_count + 1
	try:			
		prob = float(win_count)/(float(win_count) + float(loss_count)) 
	except:
		return 0,0
	return prob,float(win_count+loss_count)/float(len(training))

correct_count = 0
wrong_count = 0
counter = 1
for line in test:
	prior = [0.5,0.5]
	print 'Line Number : ' + str(counter)
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
	for i in range(len(hero_ids[:5])):
		hero_id_list = hero_ids[:i+1]
		print hero_id_list
		probability,count = find_probability(hero_id_list,training)
		if probability == 0:
			break
		if probability > 0.5:
			prior[0] = prior[0] + (probability - 0.5)*count
			prior[1] = prior[1] - (probability - 0.5)*count
		else:
			prior[1] = prior[1] + (0.5 - probability)*count
			prior[0] = prior[0] - (0.5 - probability)*count
	print prior
	if prior[0] >= prior[1]:
		predicted_result = 1
	else:
		predicted_result = 0
	if predicted_result == result:
		correct_count = correct_count + 1
		print 'Correct!!'
	else:
		wrong_count = wrong_count + 1
	counter = counter + 1
	accuracy = float(correct_count)/(float(correct_count) + float(wrong_count))
	print 'Accuracy : ' + str(accuracy) 

accuracy = float(correct_count)/(float(correct_count) + float(wrong_count))
print 'Accuracy : ' + str(accuracy) 