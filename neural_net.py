from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
tstdata, trndata = alldata.splitWithProportion(0.25)
fnn = buildNetwork(trndata.indim, 5,1, trndata.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

alldata = ClassificationDataSet(5,1, nb_classes=2)
file_handler_features = open('feature_vectors_reverse.csv','r')
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

trainer.trainEpochs(5)

trnresult = percentError( trainer.testOnClassData(),trndata['class'] )
tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )

print trnresult,tstresult

