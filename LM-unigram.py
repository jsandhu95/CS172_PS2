from __future__ import division
import sys
import math
import re
import os


documents = {}
stopwords = []
query_documents = {}
tf = {}

def parse_documents():
    global stopwords

    doc_mode = 0
    text_mode = 0
    docno = 0
    substring_doc = "<DOC>"
    substring_endDoc = "</DOC>"
    substring_text = "<TEXT>"
    substring_endText = "</TEXT>"
    substring_docno = "<DOCNO>"

    with open('stoplist.txt') as f:
        stopwords = f.read().splitlines()

    file_list = os.listdir(data_directory)

    for file in file_list:
        with open("{}/{}".format(data_directory, file)) as fp:
            for line in fp:
                if not doc_mode:
                    if substring_doc in line:
                        doc_mode = 1
                        text_mode = 0
                        docno = 0
                    continue
                if substring_endDoc in line:
                    doc_mode = 0
                    continue
                if substring_docno in line:
                    words = line.split()
                    docno = words[1]
                    documents[docno] = {}
                    tf[docno] = {}
                if not text_mode:
                    if substring_text in line:
                        if not docno:
                            continue
                        text_mode = 1
                    continue
                if substring_endText in line:
                        text_mode = 0
                else:
                    add_words(documents[docno], line)



def add_words(word_list, line):
    filter = re.sub("[^a-zA-Z ]+", "", line)
    words = filter.split()
    for word in words:
        word = word.lower()
        if word in stopwords:
            continue
        if word not in word_list:
            word_list[word] = 0
        word_list[word] += 1

def compute_documents_tf():
    global tf
    for doc in documents:
        total = 0
        for word in documents[doc]:
            total += documents[doc][word]
        for word in documents[doc]:
            tf[doc][word] = (documents[doc][word] / total) 

 
def parse_query():
    global query_documents
    global query_tf
    global query_tf_idf

    query_docno = 0

    with open(query_file) as fp:
        for line in fp:
            query_words = line.split()
            query_docno = query_words[0]
            query_documents[query_docno] = {}

            add_words(query_documents[query_docno], line)
    


def print_results(query_number, results):
    q_number = query_number.replace('.','')
    counter = 0
    f = open(results_file, "a")
    for i in sorted(results, key=results.get, reverse=True):
        if (results[i] == 0):
            break
        counter += 1
        f.write("{} Q0 {} {} {} Exp\n".format(q_number, i, counter, results[i]))
        if (counter == 20):
            break
    f.close()


def compute_lm(query):
    global tf
    lm = {}
    for doc in documents:
        lm[doc] = 0
        v = 0
        for word in documents[doc]:
            v += documents[doc][word]
        l = len(documents[doc])
        denominator = l + v
        for word in query:
            if word not in tf[doc]:
                tf[doc][word] = 0
            numerator = tf[doc][word] + 1
            lm[doc] += math.log(numerator / denominator)
    return lm



if (len(sys.argv) < 4):
    print "Usage: sys.argv[0] <document-directory> <query-file> <results-file>"
    exit()

data_directory = sys.argv[1]
query_file = sys.argv[2]
results_file = sys.argv[3]

parse_documents()
compute_documents_tf()

parse_query()
for doc in query_documents:
    results = compute_lm(query_documents[doc])
    print_results(doc, results)



    
