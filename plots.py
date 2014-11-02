import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def plot(accuracies_rf,accuracies_knn,accuracies_svm,accuracies_svm_rbf,training_data):
	y_rf = accuracies_rf
	y_knn = accuracies_knn
	y_svm = accuracies_svm
	y_svm_rbf = accuracies_svm_rbf
	x = range(len(accuracies))
	x = [i+10 for i in x]
	#f = interpolate.interp1d(x, y)
	#plt.plot(x,y,'o',x,f(x),'-',label='interpolated')
	plt.plot(x, y_rf, label='RF')
	plt.plot(x, y_knn, label='KNN')
	plt.plot(x, y_svm, label='SVM')
	plt.plot(x, y_svm_rbf, label='SVM RBF')
	plt.xlabel('Number of Samples')
	plt.ylabel('Classification Accuracy')
	plt.show()



