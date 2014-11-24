from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
import plots
from random import shuffle
from sklearn.metrics import f1_score
from sklearn.learning_curve import learning_curve

rf = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)
et = ExtraTreesClassifier()
ab = AdaBoostClassifier()
clf2 = svm.LinearSVC()
clf = svm.SVC(kernel='poly')
logreg = linear_model.LogisticRegression(C=1e5)
knn = KNeighborsClassifier(n_neighbors=5)
nc = NearestCentroid()

def populate_hero_stats(file_handler_features_heroes):
	feature_content = file_handler_features_heroes.readlines()
	hero_dict = {}
	for line in feature_content:
		line = line.strip()
		line = line.split(',')
		if len(line) > 100:
			continue
		hero_data = line[:90]
		hero_data=[hero_data[x:x+9] for x in xrange(0, len(hero_data), 9)]
		#print hero_data
		if len(hero_data) < 10:
			continue
		for hero in hero_data:
			hero_id = hero[0]
			if hero_id not in hero_dict:
				hero_dict[hero_id] = []
			kills = hero[1]
			deaths = hero[2]
			assists = hero[3]
			gpm = hero[5]
			xpm = hero[6]
			hero_damage = hero[7]
			level = hero[8]
			feature = float(kills) - float(deaths) + (float(assists)/2) + float(level) + float(gpm)/100 + float(xpm)/100 + float(hero_damage)/10000 
			hero_dict[hero_id].append(feature)

	parallel_hero_dict = {}
	for hero in hero_dict:
		hero_stats = hero_dict[hero]
		hero_stat = float(sum(hero_stats))/len(hero_stats)
		parallel_hero_dict[hero] = hero_stat
	print parallel_hero_dict
	return parallel_hero_dict

def compute_f_score(training_data,results):
	'''
	print 'Length : ' + str(len(training_data))
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	rf.fit(training_data,results_training)
	print rf.score(test_data,results_test)
	y_true = []
	y_pred = []
	for i in range(len(test_data)):
		result = rf.predict(test_data[i])
		y_true.append(int(results_test[i]))
		y_pred.append(int(result[0]))
	print f1_score(y_true,y_pred)
	'''
	train_sizes,train_scores,valid_scores = learning_curve(RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0), training_data, results, train_sizes=[1, 0.9, 0.8], cv=5)
	print train_scores
	print valid_scores

def hold_out(training_data,results):
	print 'Length : ' + str(len(training_data))
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	clf2.fit(training_data,results_training)
	print clf2.score(test_data,results_test)
	print clf2.score(training_data,results_training)

def hold_out_training(training_data,results):
	print 'Length : ' + str(len(training_data))
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	rf.fit(training_data,results_training)
	print rf.score(test_data,results_test)
	'''
	pre_shuffle_stuff = []
	counter = 0
	for item in results_training:
		item = item.append(results_training[counter])		
	accuracies = []
	#shuffle(training_data)
	'''
	accuracies_svm = []
	accuracies_rf = []
	accuracies_knn = []
	accuracies_svm_rbf = []
	for j in range(10,len(training_data),1):
		correct = 0
		wrong = 0
		curr_training_data = training_data[:j]
		curr_results = results_training[:j]
		rf.fit(curr_training_data,curr_results)	
		rf.score(test_data,results_test)
		y_true = []
		y_pred = []
		for i in range(len(test_data)):
			result = rf.predict(test_data[i])
			
			if result[0] == results_test[i]:
				correct = correct + 1
				#print 'Correct : ' + str(result)
			else:
				wrong  = wrong + 1
				#iprint 'Wrong : ' + str(result)
		print correct,wrong
		accuracy = (float(correct))/(float(correct) + float(wrong))
		accuracies_rf.append(accuracy)
		print 'Accuracy : ' + str(accuracy)
		knn.fit(curr_training_data,curr_results)
		knn.score(test_data,results_test)
		correct = 0
		wrong = 0
		for i in range(len(test_data)):
			result = knn.predict(test_data[i])
			
			if result[0] == results_test[i]:
				correct = correct + 1
				#print 'Correct : ' + str(result)
			else:
				wrong  = wrong + 1
				#iprint 'Wrong : ' + str(result)
		print correct,wrong
		accuracy = (float(correct))/(float(correct) + float(wrong))
		accuracies_knn.append(accuracy)
		print 'Accuracy : ' + str(accuracy)
		clf2.fit(curr_training_data,curr_results)
		clf2.score(test_data,results_test)
		correct = 0
		wrong = 0
		for i in range(len(test_data)):
			result = knn.predict(test_data[i])
			
			if result[0] == results_test[i]:
				correct = correct + 1
				#print 'Correct : ' + str(result)
			else:
				wrong  = wrong + 1
				#iprint 'Wrong : ' + str(result)
		print correct,wrong
		accuracy = (float(correct))/(float(correct) + float(wrong))
		accuracies_svm.append(accuracy)
		print 'Accuracy : ' + str(accuracy)
		clf.fit(curr_training_data,curr_results)
		clf.score(test_data,results_test)
		correct = 0
		wrong = 0
		for i in range(len(test_data)):
			result = knn.predict(test_data[i])
			
			if result[0] == results_test[i]:
				correct = correct + 1
				#print 'Correct : ' + str(result)
			else:
				wrong  = wrong + 1
				#iprint 'Wrong : ' + str(result)
		print correct,wrong
		accuracy = (float(correct))/(float(correct) + float(wrong))
		accuracies_svm_rbf.append(accuracy)
		print 'Accuracy : ' + str(accuracy)
	plots.plot(accuracies_rf,accuracies_knn,accuracies_svm,accuracies_svm_rbf,training_data)
	#return accuracies

def leave_one_out(training_data,test_point,results,test_result):
	rf.fit(training_data,results)
	result = rf.predict(test_point)
	if result == test_result:
		return True
	else:
		return False

def leave_one_out_classifier(training_data,results):
	correct = 0
	wrong = 0
	for i in range(len(training_data)):
		print 'Iteration : ' + str(i)
		test_point = training_data[i]
		test_result = results[i]
		remaining_training = [training_data[j] for j in range(len(training_data)) if i!=j]
		remaining_results = [results[j] for j in range(len(results)) if i!=j]
		print len(remaining_training)
		result = leave_one_out(remaining_training,test_point,remaining_results,test_result)
		if result == True:
			#print 'True'
			correct = correct + 1
		else:
			#print 'False'
			wrong = wrong + 1
		accuracy = (float(correct))/(float(correct) + float(wrong))
		print 'Accuracy : ' + str(accuracy)

def extract_features(file_handler_features,hero_dict):
	file_handler_features.seek(0)
	x = file_handler_features.readlines()
	print len(x)
	x = list(set(x))
	print len(x)
	training_data = []
	results = []
	del x[0]
	for line in x:
		line = line.strip()
		line = line.split(',')
		if len(line) <=10:
			continue
		#print line
		item = line[:10]
		#print item
		duration = int(line[11])
		if duration < 1200 or len(line) >= 20:
			continue
		item = [int(item[i]) for i in range(len(item))]
		feature_vector = [0 for i in range(231)]
		counter = 0
		for hero in item[:5]:
			feature_vector[hero] = 1
			feature_vector[221+counter] = float(hero_dict[str(hero)])
			counter = counter + 1
		for hero in item[5:]:
			feature_vector[hero+110] = 1
			feature_vector[221+counter] = float(hero_dict[str(hero)])
			counter = counter + 1
		training_data.append(feature_vector)
		results.append(int(line[10]))
	correct = 0
	wrong = 0
	return training_data,results

def extract_features_simple(file_handler_features,hero_dict):
	file_handler_features.seek(0)
	x = file_handler_features.readlines()
	training_data = []
	results = []
	del x[0]
	for line in x:
		line = line.strip()
		line = line.split(',')
		if len(line) <=10:
			continue
		#print line
		item = line[:10]
		#print item
		duration = int(line[11])
		if duration < 1200 or len(line) >= 20:
			continue
		item = [int(item[i]) for i in range(len(item))]
		feature_vector = [0 for i in range(231)]
		counter = 0
		for hero in item[:5]:
			feature_vector[hero] = 1
		for hero in item[5:]:
			feature_vector[hero+110] = 1
		training_data.append(feature_vector)
		results.append(int(line[10]))
	correct = 0
	wrong = 0
	return training_data,results

def classify(file_handler_features_heroes,file_handler_features):
	hero_dict = populate_hero_stats(file_handler_features_heroes)
	training_data,results = extract_features(file_handler_features,hero_dict)
	#training_data_simple,results_simple = extract_features_simple(file_handler_features,hero_dict)
	#training_data_1,results_1 = extract_features_heroes(file_handler_features_heroes,hero_dict)
	#leave_one_out_classifier(training_data,results)
	#leave_one_out_classifier(training_data_simple,results_simple)
	hold_out(training_data,results)