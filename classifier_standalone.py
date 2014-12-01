from sklearn import svm, linear_model
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
import random
import plots

model = BernoulliRBM(n_components=2)
rf = RandomForestClassifier(n_estimators=15, max_depth=15,min_samples_split=8, random_state=0, criterion='entropy',n_jobs=-1)
et = ExtraTreesClassifier()
ab = AdaBoostClassifier()
clf2 = svm.LinearSVC()
clf = svm.SVC(kernel='rbf')
logreg = linear_model.LogisticRegression(C=0.5,penalty='l2')
knn = KNeighborsClassifier(n_neighbors=5)
sgdc = SGDClassifier()
gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()
prcp = Perceptron()
rbm = BernoulliRBM(random_state=0, verbose=True)
rbm.learning_rate = 0.1
rbm.n_iter = 5
rbm.n_components = 1000

classifier = Pipeline(steps=[('rbm', rbm), ('logreg', logreg)])
file_handler_features = open('bigram_features.csv','r')

def unique(training_data,test_data):
	for item in training_data:
		if item in test_data:
			print 'Item in test'

def hold_out(training_data,results):
	print 'Total Data : ' + str(len(training_data))
	print sum(results);
	test_data = training_data[-int(0.1*len(training_data)):]
	training_data = training_data[:-int(0.1*len(training_data))]
	results_training = results[:-int(0.1*len(results))]
	results_test = results[-int(0.1*len(results)):]
	zeros = 0
	ones = 0
	# unique(training_data,test_data)
	print 'Training Items : ' + str(len(training_data))
	print 'Test Items : ' + str(len(test_data))
	'''
	training_scores_logreg = []
	testing_scores_logreg = []
	training_scores_svm = []
	testing_scores_svm = []
	training_scores_rf = []
	testing_scores_rf = []
	training_scores_bnb = []
	testing_scores_bnb = []
	#training_scores_knn = []
	#testing_scores_knn = []
	for i in range(1,len(training_data)/500):
		logreg.fit(training_data[:i*500],results_training[:i*500])
		testing_scores_logreg.append(logreg.score(test_data,results_test))
		training_scores_logreg.append(logreg.score(training_data,results_training))
		clf2.fit(training_data[:i*500],results_training[:i*500])
		testing_scores_svm.append(clf2.score(test_data,results_test))
		training_scores_svm.append(clf2.score(training_data,results_training))
		rf.fit(training_data[:i*500],results_training[:i*500])
		testing_scores_rf.append(rf.score(test_data,results_test))
		training_scores_rf.append(rf.score(training_data,results_training))
		bnb.fit(training_data[:i*500],results_training[:i*500])
		testing_scores_bnb.append(bnb.score(test_data,results_test))
		training_scores_bnb.append(bnb.score(training_data,results_training))
		#logreg.fit(training_data[:i*500],results_training[:i*500])
		#testing_scores_logreg.append(logreg.score(test_data,results_test))
		#training_scores_logreg.append(logreg.score(training_data,results_training))
	plots.plot(training_scores_logreg,testing_scores_logreg,training_scores_svm,testing_scores_svm ,training_scores_rf ,testing_scores_rf ,training_scores_bnb , testing_scores_bnb)
	'''
	knn.fit(training_data,results_training)
	print knn.score(test_data,results_test)
	print knn.score(training_data,results_training)
	#print rf.feature_importances_

lines = file_handler_features.readlines()
lines = list(set(lines))
results = []
training_data = []
all_data = []
for line in lines:
	line = line.strip()
	line = line.split(',')
	del line[-1]
	del line[0]
	line = [float(i) for i in line]
	#result = line[-1]
	#results.append(result)
	all_data.append(line)
	#del line[-1]
	#training_data.append(line)
#print results
#print all_data
random.shuffle(all_data)
for line in all_data:
	result = line[-1]
	results.append(result)
	del line[-1]
	training_data.append(line)


hold_out(training_data,results)


