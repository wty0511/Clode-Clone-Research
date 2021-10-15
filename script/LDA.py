import gensim
import gensim.corpora as corpora
from pprint import pprint
from gensim.models import CoherenceModel
import numpy as np
from tqdm import tqdm
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim import models
from collections import Counter
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool

def get_commit_text():
    file = open("../data/commit_message_clean_preprocessing.dic",encoding="utf-8")
    dic = json.load(file)
    file.close()

    l=[]

    count=0
    for name in dic:


        for num in dic[name]:
            text = []
            if  not type(dic[name][num]["title"])== float:
                text.extend(word_tokenize(dic[name][num]["title"]))

            if  not type(dic[name][num]["body"])== float:
                text.extend(word_tokenize(dic[name][num]["body"]))

            if len(text)>0 :
                l.append(text)
    return l
def get_pr_text():
    file = open("../data/pr_preprocess.dic",encoding="utf-8")
    dic = json.load(file)
    file.close()
    l=[]
    for name in dic:

        for num in dic[name]:
            text = []
            text.extend(word_tokenize(dic[name][num]["title"]))
            try:
                text.extend(word_tokenize(dic[name][num]["body"]))
            except:
                pass
            text.extend(word_tokenize(dic[name][num]["commit_title"]))
            text.extend(word_tokenize(dic[name][num]["commit_body"]))
            text.extend(word_tokenize(dic[name][num]["issue_comments"]))
            text.extend(word_tokenize(dic[name][num]["reviews"]))
            text.extend(word_tokenize(dic[name][num]["review_comments"]))
            for sha in dic[name][num].get("commit_comment",{}):
                    text.extend(word_tokenize(dic[name][num]["commit_comment"][sha]))
            l.append(text)


    print(len(l))
    return l

def get_code_comment():
    file = open("../data/code_comment_clean_preprocessing.dic",encoding="utf-8")
    dic = json.load(file)
    file.close()
    l=[]
    count=0

    for name in dic:
        for key in dic[name]:
            text = []
            for i in dic[name][key]["multi_line"]:
                text.extend(word_tokenize(i))
            for i in dic[name][key]["single_line"]:
                text.extend(word_tokenize(i))
            if len(text)>0:
                l.append(text)
    return l

if __name__ == '__main__':
    # Create Dictionary

    data=get_pr_text()

    id2word = corpora.Dictionary(data)
    k=200
    # Create Corpus
    texts = data

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus,normalize=False)

    corpus_tfidf = tfidf[corpus]

    '''
    #[10 ** n for n in [-3, -2, -1, 0, 1, 2, 3]]
    for alpha in [10 ** n for n in [-3, -2, -1, 0, 1, 2, 3]]:
        for eta in [10 ** n for n in [-3, -2, -1, 0, 1, 2, 3]]:
            c=0
            lda_model = gensim.models.LdaMulticore(corpus=corpus_tfidf,
                                                   id2word=id2word,
                                                   num_topics=k,
                                                   random_state=100,
                                                   chunksize=100,
                                                   passes=40,
                                                   alpha=alpha,
                                                   eta=eta)

            l=[]
            for i in lda_model.print_topics(-1,20):
                for j in i[1].split("+"):
                    l.append(j.split("*")[1])
            print(Counter(l))
            for i in dict(Counter(l)).values():
                if i>1:
                    c+=i
            print(c)
            print(alpha)
            print(eta)
            print("~~~~~~~~~~~")
            #pprint(lda_model.print_topics(-1,20))
    '''
    lda_model = gensim.models.LdaMulticore(corpus=corpus_tfidf,
                                           id2word=id2word,
                                           num_topics=k,
                                           random_state=10,
                                           chunksize=100,
                                           passes=100,
                                           alpha=1,
                                           eta=0.01)

    l = []
    for i in lda_model.print_topics(-1, 20):
        for j in i[1].split("+"):
            l.append(j.split("*")[1])
    print(Counter(l))
    pprint(lda_model.print_topics(-1, 20))

