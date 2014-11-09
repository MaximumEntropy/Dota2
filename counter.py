file_handler_feature_vectors = open('feature_vectors.csv','r')
file_handler_feature_vectors_heroes = open('feature_vectors_heroes.csv','w')
file_handler_xml_extracted = open('features_local.csv','r')
lines = file_handler_feature_vectors.readlines()
lines = list(set(lines))
zero_count = 0
one_count = 0
for line in lines:
	line = line.strip()
	line = line.split(',')
	print line[-1]
	if line[80] == '0':
		zero_count = zero_count + 1
	else:
		one_count = one_count + 1

print zero_count,one_count