import sys
import os
import argparse
import pickle

GROUP_NUMBER = 19

def readModel(model):
	with open(model, 'rb') as modelFile:
		model_dict = pickle.load(modelFile)
	return model_dict

def readQueries(QUERY_PATH):
	queries = {}
	with open(QUERY_PATH, 'r') as readFile:
		for line in readFile:
			queries[int(line.split(',')[0])] = line.split(',')[1].split('\n')[0].split(' ')
	return queries

def makeBoolFile(model, queries):
	document_bool = {}
	for query in queries:
		if query not in document_bool:
			document_bool[query] = []
		temp_list = set()
		for token in queries[query]:
			if len(temp_list) == 0 and token in model.keys():
				temp_list = set(model[token])
			elif token in model.keys():
				temp_list.intersection(set(model[token]))
		document_bool[query] = list(temp_list)
	return document_bool

def writeBooleanFile(res):
	with open('Assignment1_' + str(GROUP_NUMBER) + '_results.txt', 'w') as writeFile:
		for key in res:
			writeFile.write(str(key)+':')
			writeFile.write(" ".join(str(val) for val in res[key]))
			writeFile.write('\n')

def main(MODEL_PATH, QUERY_PATH):
	model = readModel(MODEL_PATH)
	queries = readQueries(QUERY_PATH)
	res = makeBoolFile(model, queries)
	writeBooleanFile(res)
	exit()

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='handles the file path')
	parser.add_argument('MODEL', help='path to the files, for example: .../Data/en_BDNews24')
	parser.add_argument('QUERY', help='path to the files, for example: .../Data/en_BDNews24')
	args = parser.parse_args()
	# validating the directory
	model = os.path.abspath(args.MODEL)
	if not os.path.isfile(model):
		raise Exception('Invalid file path given {}, required file should be a binary file for the query model'.format(model))
	query = os.path.abspath(args.QUERY)
	if not os.path.isfile(query):
		raise Exception('Invalid file path given {}, required file should be a text file for the query'.format(query))
	main(model, query)