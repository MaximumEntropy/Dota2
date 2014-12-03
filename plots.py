import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def plot(training_scores_logreg,testing_scores_logreg,training_scores_svm,testing_scores_svm ,training_scores_rf ,testing_scores_rf ,training_scores_bnb , testing_scores_bnb):
	#y_test = accuracies_testing
	#y_train = accuracies_training
	#y_svm = accuracies_svm
	#y_svm_rbf = accuracies_svm_rbf
	x = range(len(testing_scores_logreg))
	x = [i*1000 for i in x]
	#f = interpolate.interp1d(x, y)
	#plt.plot(x,y,'o',x,f(x),'-',label='interpolated')
	lr, = plt.plot(x, training_scores_logreg, label='Logistic Regression')
	svm, = plt.plot(x, training_scores_svm, label='SVM Linear Kernel')
	rf, = plt.plot(x, training_scores_rf, label='Random Forests')
	bnb, = plt.plot(x, training_scores_bnb, label='Bernoulli Naive Bayes')
	#plt.plot(x, y_train, label='Training')
	plt.xlabel('Number of Samples')
	plt.ylabel('Classification Accuracy')
	plt.legend([lr,svm,rf,bnb], ['Logistic Regression', 'SVM Linear Kernel','Random Forests','Bernoulli Naive Bayes'], loc='left')
	plt.ylim([0.5,0.74])
	plt.show()



