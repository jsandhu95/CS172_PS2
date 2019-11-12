from __future__ import division
import sys
import math
import re
import os


documents = {}
stopwords = []
query_documents = {}
tf = {}
idf = {}
tf_idf = {}
query_tf = {}
query_tf_idf = {}

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
                    tf_idf[docno] = {}
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

def compute_documents_idf():
    global idf
    for doc in documents:
        for word in documents[doc]:
            total = 0
            for i in documents:
                if word in documents[i]:
                    total += 1
            idf[word] = math.log(len(documents) / max(1, total)) 
    

def compute_documents_tf_idf():
    global tf_idf
    for doc in documents:
        for word in documents[doc]:
            tf_idf[doc][word] = tf[doc][word] * idf[word]
 
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
            query_tf[query_docno] = {}
            query_tf_idf[query_docno] = {}

            add_words(query_documents[query_docno], line)
    

def compute_query_tf_idf():
    global query_tf
    global query_tf_idf
    for doc in query_documents:
        for word in query_documents[doc]:
            query_tf[doc][word] = query_documents[doc][word] / len(query_documents[doc])

    for doc in query_documents:
        for word in query_documents[doc]:
            if word in idf:
                query_tf_idf[doc][word] = query_tf[doc][word] * idf[word]
            else:
                query_tf_idf[doc][word] = 0


def list_product(list1, list2):
    length = len(list1)
    total = 0
    for x in range(length):
        total = total + (list1[x] * list2[x])
    return total
            

def compute_cossim(query):
    cossim = {}
    q_list = list(query.values())
    d2 = math.sqrt(list_product(q_list, q_list))
    for doc in documents:
        d_list = compute_vector(doc, query)
        numerator = list_product(d_list, q_list)
        d1 = math.sqrt(list_product(d_list, d_list))
        denominator = d1 * d2
        if (denominator == 0):
            cossim[doc] = 0
        else:
            cossim[doc] = numerator / denominator
    return cossim

def compute_vector(docno, query):
    r_list = []
    for word in query:
        if word in documents[docno]:
            r_list.append(tf_idf[docno][word])
        else:
            r_list.append(0)
    return r_list



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






if (len(sys.argv) < 4):
    print "Usage: {} <document-directory> <query-file> <results-file>".format(sys.argv[0])
    exit()

data_directory = sys.argv[1]
query_file = sys.argv[2]
results_file = sys.argv[3]

parse_documents()
compute_documents_tf()
compute_documents_idf()
compute_documents_tf_idf()

parse_query()
compute_query_tf_idf()
for doc in query_tf_idf:
    results = compute_cossim(query_tf_idf[doc])
    print_results(doc, results)



    
