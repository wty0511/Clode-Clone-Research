import gensim
import gensim.corpora as corpora
from pprint import pprint
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import CoherenceModel
import numpy as np
from tqdm import tqdm
import logging
from gensim import models
import json
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
            if len(text)>0:
                l.append(text)


    print(len(l))
    return l



def compute_coherence_values(corpus, dictionary, k, a, b):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=k,
                                           random_state=100,
                                           chunksize=10000,
                                           passes=70,
                                           workers=16,
                                           alpha=a,
                                           eta=b)
    print("train done")
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data, dictionary=id2word, coherence='c_v')
    print("coherence")
    return coherence_model_lda.get_coherence()
def optimize(input):

    print("start")
    for par in tqdm(input,position=0):
        i, k, a, b = par

        cv = compute_coherence_values(corpus=corpus_sets[i], dictionary=id2word,
                                      k=k, a=a, b=b)
        # Save the model results
        model_results['Validation_Set'].append(corpus_title[i])
        model_results['Topics'].append(k)
        model_results['Alpha'].append(a)
        model_results['Beta'].append(b)
        model_results['Coherence'].append(cv)
        pd.DataFrame(model_results).to_csv('./lda_tuning_code_results7.csv', index=False)

def split_list_n_list(origin_list, n):


    res=[]
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1

    for i in range(0, n):
        res.append(origin_list[i * cnt:(i + 1) * cnt])
    return res
def split(n,corpus_sets,topics_range,alpha,beta):
    data=[]
    for i in range(len(corpus_sets)):
        # iterate through number of topics
        for k in topics_range:
            # iterate through alpha values
            for a in alpha:
                # iterare through beta values
                for b in beta:
                    data.append((i,k,1/k,1/k))

    return split_list_n_list(data,n)

def get_code_comment():
    file = open("../data/code_comment_clean_preprocessing.dic",encoding="utf-8")
    dic = json.load(file)
    file.close()
    l=[]
    count=0

    for name in dic:
        print(name)
        for key in dic[name]:
            text = []

            text.extend(word_tokenize(dic[name][key]["multi_line"]))
            text.extend(word_tokenize(dic[name][key]["single_line"]))
            if len(text)>0:
                l.append(text)
    return l

if __name__ == '__main__':
    # Create Dictionary


    data=get_code_comment()
    print(data)
    id2word = corpora.Dictionary(data)
    # Create Corpus
    texts = data
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    #tfidf = models.TfidfModel(corpus,normalize=False)
    #corpus_tfidf = tfidf[corpus]
    grid = {}
    grid['Validation_Set'] = {}

    # Topics range
    min_topics = 20
    max_topics = 110
    step_size = 10
    topics_range = range(min_topics, max_topics, step_size)

    # Alpha parameter
    alpha=[0.01]
    '''
    alpha = list(np.arange(0.01, 0.01, 0.3))
    alpha.append('symmetric')
    alpha.append('asymmetric')
    '''

    # Beta parameter
    beta = [100]
    '''
    beta = list(np.arange(0.01,0.01, 0.3))
    beta.append('symmetric')
    '''

    # Validation sets
    #num_of_docs = len(corpus_tfidf)
    #corpus_sets = [corpus_tfidf]
    num_of_docs = len(corpus)
    corpus_sets = [corpus]

    corpus_title = ['100% Corpus']

    model_results = {'Validation_Set': [],
                     'Topics': [],
                     'Alpha': [],
                     'Beta': [],
                     'Coherence': []
                     }

    mul = 1

    input=split(mul,corpus_title,topics_range,alpha,beta)
    count=0
    for i in input:
        count+=len(i)
    print(count)
    print(input)
    pool = ThreadPool(processes=mul)
    pool.map(optimize,input)
    #optimize(input[0])
    pool.close()
    pool.join()




