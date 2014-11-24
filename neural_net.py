from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.datasets import SupervisedDataSet
ds = ClassificationDataSet(220,1)
file_handler_features = open('feature_vectors.csv','r')
lines = file_handler_features.readlines()
lines = list(set(lines))
for line in lines:
	line = line.strip()
	line = line.split(',')
	del line[-1]
	del line[0]
	line = [float(i) for i in line]
	result = line[-1]
	ds.addSample(tuple(line[:-1]),tuple([result]))

tstdata, trndata = ds.splitWithProportion( 0.25 )
fnn = buildNetwork(ds.indim, 5,1, trndata.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)
trainer.trainUntilConvergence()
out = fnn.activateOnDataset(tstdata)
print out

'''
for i in range(20):
	trainer.trainEpochs(1)
	trnresult = percentError( trainer.testOnClassData(),trndata['class'] )
	tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )
	print "epoch: %4d" % trainer.totalepochs, "  train error: %5.2f%%" % trnresult, "  test error: %5.2f%%" % tstresult
'''
