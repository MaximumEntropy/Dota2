from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier

rf = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)
et = ExtraTreesClassifier()
ab = AdaBoostClassifier()
clf2 = svm.LinearSVC()
clf = svm.SVC()
logreg = linear_model.LogisticRegression(C=1e5)

def hold_out_training(training_data,results):
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	et.fit(training_data,results_training)
	correct = 0
	wrong = 0
	for i in range(len(test_data)):
		result = et.predict(test_data[i])
		if result == results_test[i]:
			correct = correct + 1
			print 'Correct : ' + str(result)
		else:
			wrong  = wrong + 1
			print 'Wrong : ' + str(result)
	print correct,wrong
	accuracy = (float(correct))/(float(correct) + float(wrong))
	print 'Accuracy : ' + str(accuracy)

def leave_one_out(training_data,test_point,results,test_result):
	rf.fit(training_data,results)
	result = rf.predict(test_point)
	if result == test_result:
		return True
	else:
		return False

def leave_one_out_classifier(training_data,results):
	for i in range(len(training_data)):
		print 'Iteration : ' + str(i)
		test_point = training_data[i]
		test_result = results[i]
		remaining_training = [training_data[j] for j in range(len(training_data)) if i!=j]
		remaining_results = [results[j] for j in range(len(results)) if i!=j]
		print len(remaining_training)
		result = leave_one_out(remaining_training,test_point,remaining_results,test_result)
		if result == True:
			print 'True'
			correct = correct + 1
		else:
			print 'False'
			wrong = wrong + 1
		accuracy = (float(correct))/(float(correct) + float(wrong))
		print 'Accuracy : ' + str(accuracy)

def extract_features():
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
		feature_vector = [0 for i in range(231)]
		for hero in item[:5]:
			feature_vector[hero] = 1
		for hero in item[5:]:
			feature_vector[hero+110] = 1
		training_data.append(feature_vector)
		results.append(int(line[10]))
	correct = 0
	wrong = 0
	return training_data,results

def extract_features_heroes():
	x = file_handler_features_heroes.readlines()
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
		feature_vector = [0 for i in range(231)]
		for hero in item[:5]:
			feature_vector[hero] = 1
		for hero in item[5:]:
			feature_vector[hero+110] = 1
		training_data.append(feature_vector)
		results.append(int(line[10]))
	correct = 0
	wrong = 0
	return training_data,results