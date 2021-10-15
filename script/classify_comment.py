import pickle
import json
from tqdm import tqdm
from nltk.tokenize import sent_tokenize, word_tokenize
from random import randint, sample
def word_feats(words):
    return dict([(word, True) for word in words])



#Classification of SATD

f = open('../data/code_comment_clean.dic', mode='r', encoding="utf-8")
dic = json.load(f)
f.close()
text=[]
for name in dic:
    for sha in tqdm(dic[name],position=0):
        text.extend(dic[name][sha]["multi_line"])
        text.extend(dic[name][sha]["single_line"])

text=list(set(text))
print(len(text))
dic={}
t=[]

for x in text:
    t.append(x.lower())
for i in range(10):
    f = open("../data/maximum_entropy_model/" + str(i + 1) + ".pickle", 'rb')
    classifier = pickle.load(f)
    for i in t:
        observed = classifier.classify(word_feats(word_tokenize(i)))
        temp=dic.get(i, [])
        temp.append(observed)
        dic[i]=temp

for key in dic:
    dic[key]=max(dic[key],key=dic[key].count)

