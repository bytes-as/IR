import sys
import os
import argparse
import xml.etree.ElementTree as ET
import re
import string
# import pickle
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
# from nltk.stem.porter import PorterStemmer

GROUP_NUMBER = 19

class Query:
	def __init__(self, number, title, desc, narr, lang='en'):
		self.id = number
		self.title = title
		self.desc = desc
		self.narr = narr
		self.lang = lang

	def printQuery(self, ):
		print('[QUERY ID \'' + self.lang + '\']:', self.id)
		print('[%-13s]:%s'%('QUERY TITLE', self.title))
		print('[%-13s]:%s'%('QUERY DESC', self.desc))
		print('[%-13s]:%s'%('QUERY NARR', self.narr))
		print('-------------------------------------------------------------->')

def cleanText(text):
	# punctuations removal and tokenization
	text = "".join([alpha for alpha in text if alpha not in string.punctuation])
	# tokenize
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(text.lower())
	# remove stop words
	words = [word for word in words if not word in stopwords.words('english')]
	# lemmanization
	lemmatizer = WordNetLemmatizer()
	words = [lemmatizer.lemmatize(word) for word in words]
	return words

def writeQuery(queries, write_file):
	print('[QUERIES WRITING]: Strating...')
	with open(write_file, 'w') as writeFile:
		for query in queries:
			words = cleanText(query.title)
			writeFile.write(query.id)
			writeFile.write(',')
			writeFile.write(" ".join(words))
			writeFile.write('\n')
	print('[QUERIES WRITING]: Finished writing. :)')


def main(FILE_PATH):
	print('[READING]:', FILE_PATH)
	tree = ET.parse(FILE_PATH)
	tree.getroot()
	queries = []
	for topic in tree.findall('top'):
		language = topic.attrib['lang']
		number = topic.find('num').text
		title = topic.find('title').text
		desc = topic.find('desc').text
		narr = topic.find('narr').text
		queries.append(Query(number, title, desc, narr, lang=language))
	for query in queries:
		query.printQuery()
	writeFile = './queries_' + str(GROUP_NUMBER) + '.txt'
	writeQuery(queries, writeFile)
	exit()

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='handles the file path')
	parser.add_argument('FILE_PATH', help='path to the files, for example: .../Data/en_BDNews24')
	args = parser.parse_args()
	# validating the directory
	FILE_PATH = os.path.abspath(args.FILE_PATH)
	if not os.path.isfile(FILE_PATH) or not '/Data/' in args.FILE_PATH:
		raise Exception('Invalid Directory given {}, required directory should look like this {}'.format(args.FILE_PATH, '.../Data/'))
	main(os.path.abspath(FILE_PATH))