g = open('match_features_heroes.csv','r')
y = g.readlines()
examples = []
for example in list(set(y)):
	example = example.strip()
	example = example.split(',')
	example = example[:90]
	example=[example[x:x+9] for x in xrange(0, len(example), 9)]
	examples.append(example)
print len(examples)
print len(list(set(examples)))
