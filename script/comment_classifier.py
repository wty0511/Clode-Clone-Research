# coding: utf-8

# In[1]:
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import MaxentClassifier
from nltk.corpus import movie_reviews
from nltk.metrics import scores
from nltk import precision
import itertools
import pickle
from sklearn.metrics import average_precision_score

import random
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import *
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
import operator
from imblearn.under_sampling import NearMiss

from random import randint, sample


def subset(alist, idxs):

    '''
        用法：根据下标idxs取出列表alist的子集
        alist: list
        idxs: list
    '''
    sub_list = []
    for idx in idxs:
        sub_list.append(alist[idx])

    return sub_list


def split_list(alist, group_num=4, shuffle=True, retain_left=False):
    '''
        用法：将alist切分成group个子列表，每个子列表里面有len(alist)//group个元素
        shuffle: 表示是否要随机切分列表，默认为True
        retain_left: 若将列表alist分成group_num个子列表后还要剩余，是否将剩余的元素单独作为一组
    '''

    index = list(range(len(alist)))  # 保留下标

    # 是否打乱列表
    if shuffle:
        random.shuffle(index)

    elem_num = len(alist) // group_num  # 每一个子列表所含有的元素数量
    sub_lists = {}

    # 取出每一个子列表所包含的元素，存入字典中
    for idx in range(group_num):
        start, end = idx * elem_num, (idx + 1) * elem_num
        sub_lists['set' + str(idx)] = subset(alist, index[start:end])

    # 是否将最后剩余的元素作为单独的一组
    if retain_left and group_num * elem_num != len(index):  # 列表元素数量未能整除子列表数，需要将最后那一部分元素单独作为新的列表
        sub_lists['set' + str(idx)]=sub_lists['set' + str(idx)].extend(subset(alist, index[end:]))

    return sub_lists


def best_word_feats(words):
    return dict([(word, True) for word in words if word in bestwords])

def word_feats(words):
    return dict([(word, True) for word in words])

def best_bigram_word_feats(words,score_fn=BigramAssocMeasures.chi_sq,n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_feats(words))
    return d



def evaluate_classifier(featx):

    neg = []
    pos = []

    df=pd.read_csv("../data/technical_debt_dataset_clean.csv")
    df.dropna(axis=0, how='any',inplace=True)

    for tup in df.itertuples():

        if tup[2]!= "WITHOUT_CLASSIFICATION":
            pos.append(tup[3])
        else:
            neg.append(tup[3])
    pos=list(set(pos))
    neg = list(set(neg))
    negfeats_all = []
    posfeats = []
    for f in neg:
        negfeats_all.append((featx(word_tokenize(f)), 'neg'))
    for f in pos:
        posfeats.append((featx(word_tokenize(f)), 'pos'))
    print(len(negfeats_all))
    print(len(posfeats))
    for c in range(10):
        #negfeats=sample(negfeats_all,3250)
        negfeats=negfeats_all
        #print(len(negfeats))
        #print(len(posfeats))
        random.shuffle(negfeats)
        random.shuffle(posfeats)

        #negfeats = sample(negfeats,4044)
        lenNegFeats = len(negfeats)
        lenPosFeats = len(posfeats)
        negcutoff = int(lenNegFeats * 7 / 10)
        poscutoff = int(lenPosFeats * 7 / 10)

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:lenNegFeats] + posfeats[poscutoff:lenPosFeats]

        classifier = MaxentClassifier.train(trainfeats, algorithm="GIS",max_iter=2)
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        Y_test = []
        y_score = []
        for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
            Y_test.append(label)
            d = classifier.prob_classify(feats)
            y_score.append(d.prob('pos'))
        evaluationMetrics = {}

        classifier.show_most_informative_features()
        print("==================")
        evaluationMetrics['accuracy'] = nltk.classify.util.accuracy(classifier, testfeats)
        evaluationMetrics['posPrec'] = nltk.precision(refsets['pos'], testsets['pos'])
        evaluationMetrics['posRecall'] = nltk.recall(refsets['pos'], testsets['pos'])
        evaluationMetrics['posF_Score'] = nltk.f_measure(refsets['pos'], testsets['pos'])
        evaluationMetrics['negPrec'] = nltk.precision(refsets['neg'], testsets['neg'])
        evaluationMetrics['negRecall'] = nltk.recall(refsets['neg'], testsets['neg'])
        evaluationMetrics['negF_Score'] = nltk.f_measure(refsets['neg'], testsets['neg'])
        print('accuracy:{}'.format(evaluationMetrics['accuracy']))
        print('posPrec:{}'.format(evaluationMetrics['posPrec']))
        print('posRecall:{}'.format(evaluationMetrics['posRecall']))
        print('posF_Score:{}'.format(evaluationMetrics['posF_Score']))
        print('negPrec:{}'.format(evaluationMetrics['negPrec']))
        print('negRecall:{}'.format(evaluationMetrics['negRecall']))
        print('negF_Score:{}'.format(evaluationMetrics['negF_Score']))
        average_precision = average_precision_score(Y_test, y_score, pos_label='pos')
        print(average_precision)

        #f = open("../data/maximum_entropy_model/"+str(c+1)+".pickle", 'wb')
        #pickle.dump(classifier, f)
        #f.close()


word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

testNegWords = movie_reviews.words(categories=['pos'])
testPosWords = movie_reviews.words(categories=['neg'])

for word in testNegWords:
    word_fd[word.lower()] += 1
    label_word_fd['neg'][word.lower()] += 1
for word in testPosWords:
    word_fd[word.lower()] += 1
    label_word_fd['pos'][word.lower()] += 1

pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()
total_word_count = pos_word_count + neg_word_count

word_scores = {}

for word, freq in word_fd.items():
    pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
    neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
    word_scores[word] = pos_score + neg_score

best1 = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)[:10000]
bestwords = set([w for w, s in best1])

evaluations = []
evaluations.append(evaluate_classifier(word_feats))

# evaluations.append(evaluate_classifier(best_bigram_word_feats,BigramAssocMeasures.chi_sq))




