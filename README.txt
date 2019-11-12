############### VSM.py #################

VSM.py is a vector-space model that parses through a document set and a query and extrapolates vital information. It uses this information to create a retrieval model and determine which documents are the most relevant based on the query.

The parse_documents() function extracts the document number from the beginning of the <DOC> section.
It then extracts all the words in the document in betwen the <TEXT> and </TEXT> flags.
It then removes all the stopwords and any numbers or punctuation. It then converts all the words to lower case.
The removal of stopwords is dependant on the file being named stoplist.txt and being in the same directory as VSM.py
It stores all the unique words in a python dictionary and counts how many times each unique word occurs per document.
parse_documents() also counts the total number of words in a document, not including stopwords.
parse_documents() parses through all the documents at once and indexes them in one function.

The parse_query() functions similarly to the parse() function except it is used for the query.
It extracts the query number as well as all the words in the query that aren't stop words.
It also puts all the words in a python dictionary and records the count of each unique word per query.
It does this by reading all the queries at once and indexing them into the dictionary in the same function.

The addwords() function is what is used to populate dictionaries.
addwords() is used in both parse_documents() and parse_query().
The removal of stopwords, punctuation, and numbers is done in this function. Changing all words to lowercase is also done here.
This function also counts the occurances of each unique word in the document or query.

VSM.py also has many compute functions.
It uses the information gathered in the two parse functions to compute the values needed for the vector-space model.
compute_documents_tf(), compute_documents_idf(), and compute_documents_tf_idf() are used to compute the document sets tf, idf, and tf-idf of each word, respectively.
compute_query_tf_idf() is used to get the tf-idf values of each word in each query.
compute_cossim() is used to get the cosine similarity between each query and each document.

compute_cossim() populates another dictionary which contains the cosine similarity values of each query with each document.
It does this by getting a query passed to it and computing the relevance score for each document based on that query.
This dictionary is used to get the top 20 relevant documents for each query.
compute_vector() and list_product() are two functions used in getting values needed for compute_cossim().

print_results() is used to print the top 20 values to a file.
The cosine similarity library is passed to it and it writes the 20 most relevant documents to a file.
This file can be chosen as a command line argument.

How to run:
Running this function requires 3 command line arguments.
1. The first is a path to the directory which contains the document files. The parse_documents() and parse_query() functions can extrapolate documents from multiple files so long as they follow the same structure convention. ie using <DOC> and <TEXT> flags.
2. The second is the path to the file containing the queries. 
3. The third is the name of the results file. The print_results() function will create a file of a specified name if one doesn't exist. If one does exist, it will over-write the contents of that file with the top 20 results retrieved from the retrieval model.
Example: python VSM.py <data-directory> <query-file> <results-file>
Example: python VSM.py data data/query_list.txt vsm_results.txt



############## LM-unigram.py ###############

This is a unigram Language model that parses through documents and queries and determines which documents are the most relevant based on the query.

This program uses a similar set up to the VSM.py program.

LM-unigram.py uses many of the same functions as VSM.py.
It uses the exact same parse_documents(), parse_query(), addwords(), compute_documents_tf(), and print_results() functions.
It uses these same functions because for both retrieval models, the documents and queries need to be parsed. Many of the same values are needed to compute the language model as the cosine similary, therefore I used the same functions.

The main difference is that LM-unigram.py has another compute function.
compute_lm() gets a query passed to it and creates a dictionary which contains the relevance score for each document based on that query.
It works similarly to compute_cossim() but uses a different equation to compute a different score.

This library is then passed to print_results() which uses it to write the results to a file.

How to run:
Running this function requires 3 command line arguments.
1. The first is a path to the directory which contains the document files. The parse_documents() and parse_query() functions can extrapolate documents from multiple files so long as they follow the same structure convention. ie using <DOC> and <TEXT> flags.
2. The second is the path to the file containing the queries. 
3. The third is the name of the results file. The print_results() function will create a file of a specified name if one doesn't exist. If one does exist, it will over-write the contents of that file with the top 20 results retrieved from the retrieval model.
Example: python LM-unigram.py <data-directory> <query-file> <results-file>
Example: python LM-unigram.py data data/query_list.txt lm_results.txt



################ trec_eval.pl ##############
trec_eval.pl is used along with qrels.txt to test the accuracy of the retrieval models.
Due to the minimal overlap of the queries and documents, trec_eval returned a value of 0 across the board.
Every query and every document had a uninterpolated mean-average-precision of 0 for both retrieval models.
The precision at 10 and at 30 were also 0 for all queries and documents for both retrieval models.
This would lead me to believe that none of the documents in the document sets were very relevant for any of the queries in query_list.txt.
A larger data set or more accurate queries would increase the precision values, but the ones provided were not accurate enough to determine which retrieval model was more accurate.

