###############   GROUP 19   ###################
''''  ARUN SINGH        -   16CS10008		''''
''''  PRASHANT BANJARE  -   19CS60R69		''''
################################################

######### ---indexer.py file ###############
@packages:
	argparse: for the handling of command line arguments,
	(1.1)	they could have handled with sys package of python
		but when it comes to the large number of arguments
		it's convinent to use the argparse plus it is easier
		to use

	xml     : for parsing the file in the XML like format, xml
	(0.1.1)	package's ElementTree module makes it easy to move
		around the hierarchical structure of the dat in the
		file
		NOTE: using the xml encoding the '&' is a escape
			character, so many files can't be parsed
			using this, for that I also have written
			the simple text like parsing module,
			though decided not to use it for
			consistency issues

	re      : for cleaning the data
	(2.2.1)

	pickle  : to save the dictionary results
	()

	string  : removing punctuations
	(included in python)

	nltk    : tokenization and lemmatization 
	(3.4.5)

@output:
	model_queries_19.pth is a dictionary binary file corresponding to
	the keys as the token and the list of file names as the values

To Run:
    $python Assignment1_19_indexer.py ./Data/en_BDNews24


######### ---parser.py file ###############
@packages:
	argparse: for the handling of command line arguments,
	(1.1)	

	xml     : 

	re      : for cleaning the data
	(2.2.1)

	pickle  : to save the dictionary results
	()

	string  : removing punctuations
	(included in python)

	nltk    : tokenization and lemmatization 
	(3.4.5)

@Output:
	queries_19.txt is the file having the queries with the
	<query number>, <[tokens present in the query]>

To Run:
    $python Assignment1_19_parser.py ./Data/raw_query.txt


######### ---bool.py file ###############
@packages:
	argparse: for the handling of command line arguments,
	(1.1)	

	pickle  : to read the dictionary results
	()

@Output:
	it saves the file Assignment1_19_results.txt, using the AND encoding
	it finds all the files which have the all the tokens present in the
	query and compile a list of such files and saves them in this file.

To Run:
    $python Assignment1_19_bool.py ./model_queries_19_.pth ./queries_19.txt


