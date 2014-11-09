from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.linear_model import ARDRegression, LinearRegression
from sklearn.ensemble import RandomForestRegressor

clf = linear_model.Ridge (alpha = .5)
svr = SVR(kernel='linear')
lasso = linear_model.Lasso(alpha = 0.1)
ardr = ARDRegression()
rf = RandomForestRegressor()
lr = LinearRegression()
def hold_out(training_data,results):
	test_data = training_data[-int(0.1*len(training_data)):]
	training_data = training_data[:-int(0.1*len(training_data))]
	results_training = results[:-int(0.1*len(results))]
	results_test = results[-int(0.1*len(results)):]
	print 'Training Items : ' + str(len(training_data))
	print 'Test Items : ' + str(len(test_data))
	clf.fit(training_data,results_training)
	print clf.score(test_data,results_test)
	print clf.score(training_data,results_training)
	correct = 0
	wrong = 0
	for i in range(len(test_data)):
		value = clf.predict(test_data[i])
		if value < 0:
			prediction = 0
		else:
			prediction = 1
		if results_test[i] < 0:
			actual_result = 0
		else:
			actual_result = 1
		if prediction == actual_result:
			correct = correct + 1
		else:
			wrong = wrong + 1
	print correct,wrong
	print float(correct)/(float(correct) + float(wrong))

file_handler_features = open('features_regression.csv','r')
lines = file_handler_features.readlines()
lines = list(set(lines))
results = []
training_data = []
for line in lines:
	line = line.strip()
	line = line.split(',')
	del line[-1]
	del line[0]
	line = [float(i) for i in line]
	result = line[-1]
	results.append(result)
	del line[-1]
	training_data.append(line)

hold_out(training_data,results)