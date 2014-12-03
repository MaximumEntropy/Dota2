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
from sklearn.decomposition import ProjectedGradientNMF
from sklearn.decomposition import PCA
from sklearn.lda import LDA
#from sklearn.decomposition import ICA
import random
import plots
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

model = BernoulliRBM(n_components=2)
rf = RandomForestClassifier(n_estimators=15, max_depth=15,min_samples_split=8, random_state=0, criterion='entropy',n_jobs=-1)
et = ExtraTreesClassifier()
ab = AdaBoostClassifier()
clf2 = svm.LinearSVC(penalty='l1',loss='l2',C=100,dual=False)
clf = svm.SVC(kernel='rbf')
logreg = linear_model.LogisticRegression(C=100,penalty='l2')
knn = KNeighborsClassifier(n_neighbors=5)
sgdc = SGDClassifier()
gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()
prcp = Perceptron()
rbm = BernoulliRBM(random_state=0, verbose=True)
rbm.learning_rate = 0.02
rbm.n_iter = 20
rbm.n_components = 1000
NMF = ProjectedGradientNMF(n_components=2, init='random',random_state=0)
PCA = PCA()
LDA = LDA()
#ICA = ICA()


classifier = Pipeline(steps=[('rbm', rbm), ('logreg', logreg)])
file_handler_features = open('feature_vectors_heroes.csv','r')

def unique(training_data,test_data):
	for item in training_data:
		if item in test_data:
			print 'Item in test'

def hold_out(training_data,results):
	print 'Total Data : ' + str(len(training_data))
	print sum(results);
	test_data = training_data[-int(0.2*len(training_data)):]
	training_data = training_data[:-int(0.2*len(training_data))]
	results_training = results[:-int(0.2*len(results))]
	results_test = results[-int(0.2*len(results)):]
	zeros = 0
	ones = 0
	# unique(training_data,test_data)
	print 'Training Items : ' + str(len(training_data))
	print 'Test Items : ' + str(len(test_data))
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
	for i in range(1,len(training_data)/1000):
		print 'Iteration : ' + str(i)
		print len(testing_scores_logreg)
		logreg.fit(training_data[:i*1000],results_training[:i*1000])
		testing_scores_logreg.append(logreg.score(test_data,results_test))
		training_scores_logreg.append(logreg.score(training_data,results_training))
		clf2.fit(training_data[:i*1000],results_training[:i*1000])
		testing_scores_svm.append(clf2.score(test_data,results_test))
		training_scores_svm.append(clf2.score(training_data,results_training))
		rf.fit(training_data[:i*1000],results_training[:i*1000])
		testing_scores_rf.append(rf.score(test_data,results_test))
		training_scores_rf.append(rf.score(training_data,results_training))
		bnb.fit(training_data[:i*1000],results_training[:i*1000])
		testing_scores_bnb.append(bnb.score(test_data,results_test))
		training_scores_bnb.append(bnb.score(training_data,results_training))
		#logreg.fit(training_data[:i*1000],results_training[:i*1000])
		#testing_scores_logreg.append(logreg.score(test_data,results_test))
		#training_scores_logreg.append(logreg.score(training_data,results_training))
	plots.plot(training_scores_logreg,testing_scores_logreg,training_scores_svm,testing_scores_svm ,training_scores_rf ,testing_scores_rf ,training_scores_bnb , testing_scores_bnb)
	'''
	clf2.fit(training_data,results_training)
	print clf2.score(test_data,results_test)
	print clf2.score(training_data,results_training)
	#print rf.feature_importances_
	'''

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

#training_data = PCA.fit_transform(training_data)
#print len(training_data[0])
print 'PCA Done ... '
'''
plot_data_x = []
plot_data_y = []
plot_data_z = []
colors = []
for i in range(len(training_data)):
	plot_data_x.append(training_data[i][0])
	plot_data_y.append(training_data[i][1])
	if results[i] == 1:
		plot_data_z.append(training_data[i][2])
	else:
		plot_data_z.append(training_data[i][2])
	if results[i] == 1:
		colors.append('red')
	else:
		colors.append('blue')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(plot_data_x,plot_data_y,plot_data_z,c=colors)
plt.show()
'''
hold_out(training_data,results)


