from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid

rf = RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=1, random_state=0)
et = ExtraTreesClassifier()
ab = AdaBoostClassifier()
clf2 = svm.LinearSVC()
clf = svm.SVC(kernel='poly')
logreg = linear_model.LogisticRegression(C=1e5)
knn = KNeighborsClassifier(n_neighbors=5)

file_handler_features = open('feature_vectors.csv','r')

def unique(training_data,test_data):
	for item in training_data:
		if item in test_data:
			print 'Item in test'

def hold_out(training_data,results):
	print 'Total Data : ' + str(len(training_data))
	test_data = training_data[-int(0.3*len(training_data)):]
	training_data = training_data[:-int(0.3*len(training_data))]
	results_training = results[:-int(0.3*len(results))]
	results_test = results[-int(0.3*len(results)):]
	unique(training_data,test_data)
	training_data = training_data[:20]
	results_training = results_training[:20]
	print 'Training Items : ' + str(len(training_data))
	print 'Test Items : ' + str(len(test_data))
	ab.fit(training_data,results_training)
	print ab.score(test_data,results_test)
	print ab.score(training_data,results_training)
	correct = 0
	wrong = 0
	for i in range(len(test_data)):
		result = ab.predict(test_data[i])
		if result == results_test[i]:
			correct = correct + 1
		else:
			wrong = wrong + 1
	Accuracy = (float(correct))/(float(correct)+float(wrong))
	print 'Accuracy : ' + str(Accuracy)

lines = file_handler_features.readlines()
lines = list(set(lines))
results = []
training_data = []
for line in lines:
	line = line.strip()
	line = line.split(',')
	del line[-1]
	line = [int(i) for i in line]
	result = line[-2]
	results.append(result)
	del line[-1]
	training_data.append(line)

hold_out(training_data,results)


