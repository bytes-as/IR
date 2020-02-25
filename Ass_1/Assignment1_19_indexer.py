import sys
import os
import argparse
import xml.etree.ElementTree as ET
import re
import string
import pickle
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

GROUP_NUMBER = 19

class Article:
    def __init__(self, path, doc_no, title, text, ):
        self.path = path
        self.doc_no = doc_no
        self.id = self.doc_no
        self.title = title
        self.text = text
        self.words = None

    def processText(self, verbose=False):
        if verbose:
            print('[ClEANING TEXT]: Starting...')
        # punctuations removal and tokenization
        self.text = "".join([alpha for alpha in self.text if alpha not in string.punctuation])
        # tokenize
        tokenizer = RegexpTokenizer(r'\w+')
        self.words = tokenizer.tokenize(self.text.lower())
        # remove stop words
        self.words = [word for word in self.words if not word in stopwords.words('english')]
        # lemmanization
        lemmatizer = WordNetLemmatizer()
        self.words = [lemmatizer.lemmatize(word) for word in self.words]
        if verbose:
            print('[CLEANING TEXT]: Done...')

def readArticle(file_path, parser):
    if parser=='XML':
        return parseArticleLikeXML(file_path)
    else:
        return parseArticleLikeText(file_path)

def parseArticleLikeText(file_path):
    print('[READING]: Creating ARTICLE Object for file:', file_path)
    with open(file_path, 'r') as readFile:
        document = [line for line in readFile]
    running_text = False
    texts = []
    for line in document:
        if line.startswith('</TEXT>'):
            running_text = False
        if running_text:
            texts.append(line)
        elif line.startswith('<DOCNO>') and not running_text:
            doc_id = line.split('<DOCNO>')[1].split('</DOCNO>')[0]
        elif line.startswith('<TITLE>') and not running_text:
            title = line.split('<TITLE>')[1].split('</TITLE>')[0]
        if line.startswith('<TEXT>'):
            running_text = True
    return Article(file_path, doc_id, title, "\n".join(texts))

def parseArticleLikeXML(file_path):
    # print('file path:', file_path)
    if not os.path.isdir('/tmp'):
        raise Exception('YOU MUST BE USING WINDOWS!!! SAD FOR YOU,\
                         ANYWAY JUST CAHNGE THE FUNCTION YOU ARE USING\
                         FOR CREATING ARTICLE OBJECT WITH FILE PATH AS ARGUMENT')
    with open('/tmp/temp_article', 'w') as writeFile:
        with open(file_path, 'r') as readFile:
            for line in readFile:
                line = line.replace('&', '&amp;')
                # line = line.replace('>', '&gt;')
                # line = line.replace('<', '&lt;')
                # line = line.replace("'", '&apos;')
                # line = line.replace('"', '&quot;')
                # re.sub('&', '&amp;', line)
                # re.sub('<', '&lt;', line)
                # re.sub('>', '&gt;', line)
                # re.sub("'", "&apos;", line)
                # re.sub('"', '&quot;', line)
                writeFile.write(line)
    tree = ET.parse('/tmp/temp_article')
    tree.getroot()
    title = tree.find('TITLE').text
    doc_no = tree.find('DOCNO').text
    text = tree.find('TEXT').text
    text = text.replace('&amp;', '&')
    # text = text.replace('&apos;', '\'')
    # text = text.replace('&quot;', '\"')
    return Article(file_path, doc_no, title, text)

def generateInvertIndex(articles, total=10000000):
    invertedIndex = {}
    if not isinstance(articles, list):
        raise Exception('Expecting a list of object of type <Article>, got {}'.format(str(type(articles))))
    count = 0
    for article in articles:
        if not isinstance(article, Article):
            raise Exception('Expecting a object of the type <Article>, not {}'.format(type(article)))
        article.processText(verbose=False)
        for word in article.words:
            if word not in invertedIndex:
                invertedIndex[word] = [article.id]
            else:
                invertedIndex[word].append(article.id)
        count += 1
        break
        if count % 100 == 0:
            print("Articles {}/{} completed...".format(count, total))
    return invertedIndex


def main(FILES_PATH, args):
    print(FILES_PATH)
    articles = []
    count = 0
    print('[READING FILES]: started...')
    for walks in os.walk(FILES_PATH):
        (root, dirs, files) = walks
        for file in files:
            file_path = str(root + '/' + file)
            # print(file_path)
            try:
                articles.append(readArticle(file_path, args.parser))
                # print(file_path)
            except:
                # print('leaving the file of path:', file_path)
                pass
            if count % 100 == 0:
                print(count, 'files readed')
            count += 1
            # break
    print('[READING FILES]: finished')
    print(len(articles),'/', count)
    invert_index = generateInvertIndex(articles, total = count)
    # sorting before writing
    sorted_keys = list(invert_index.keys())
    sorted_keys.sort()
    invert_index = {key: invert_index[key] for key in sorted_keys}
    print('[WRITING FILE]: strating....')
    print(invert_index)
    print(type(invert_index))
    write_file = './model_queries_' + str(GROUP_NUMBER) + '.pth' 
    with open(write_file, 'wb') as writeFile:
        pickle.dump(invert_index, writeFile)
    print('[WRITING FILE]: finished')
    exit()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='handles the file path')
    parser.add_argument('FILES_DIR', help='path to the files, for example: .../Data/en_BDNews24')
    parser.add_argument('--parser', default='XML', help='Parser using which the documents are being read, could be XML or anything else for normal read')
    args = parser.parse_args()
    # validating the directory
    FILES_PATH = os.path.abspath(args.FILES_DIR)
    if not os.path.isdir(FILES_PATH) or not '/Data/en_BDNews24' in args.FILES_DIR:
        raise Exception('Invalid Directory given {}, required directory should look like this {}'.format(args.FILES_DIR, '.../Data/en_BDNews24'))
    main(os.path.abspath(args.FILES_DIR), args)
