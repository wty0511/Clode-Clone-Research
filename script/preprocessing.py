import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
from nltk.corpus import wordnet
from collections import  Counter
from tqdm import tqdm
import pkg_resources
from nltk.stem import WordNetLemmatizer
from multiprocessing.dummy import Pool as ThreadPool
from symspellpy.symspellpy import SymSpell, Verbosity
import os
from nltk.stem.porter import PorterStemmer
word_full = set(nltk.corpus.words.words())
stopWords = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()


sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "../data/frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename(
    "symspellpy", "../data/frequency_bigramdictionary_en_243_342.txt")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)



def RemoveNonEnglishWords(sent):

    english_words = [w for w in sent if w.lower() in word_full]
    return english_words

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def stemmer(words):
    ps = PorterStemmer()
    correct = []
    for w in words:
        correct.append(ps.stem(w))
    return correct

def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)
def spellChecker(input_term):
    # maximum edit distance per dictionary precalculation

    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    return suggestions[0].term

def remove_less_than_three(sent):

    s=re.sub(r'\b\w{1,2}\b', '',sent)
    s=re.sub(r' +', ' ', s)
    return s

def Remove_Stop_word(sent):
    res=[]
    for word in word_tokenize(sent):
        if word not in stopWords:
            res.append(word)
    #res = RemoveNonEnglishWords(res)
    return " ".join(res)
def lemmatizer(text):
    wordnet_lemmatizer = WordNetLemmatizer()
    #tagged_sent = nltk.pos_tag(text)
    lemmas_sent = []
    for word in word_tokenize(text):
        lemmas_sent.append(wordnet_lemmatizer.lemmatize(word, pos="v"))  # 词形还原
    return " ".join(lemmas_sent)

l=[]
#tagged_sent = nltk.pos_tag(tokens)

def clean(input):

    input = remove_less_than_three(input)
    input = Remove_Stop_word(input)
    input = spellChecker(input)
    input = lemmatizer(input)
    input = remove_less_than_three(input)
    input = Remove_Stop_word(input)
    input= re.sub(r" +"," ",input)
    temp=[]
    for i in word_tokenize(input):
        if check(i):
            temp.append(i)
        else:
            print(input)
            print("---------")
    return " ".join(temp)


def processing():
    f = open('../data/pr_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()

    for name in dic:

        for num in tqdm(dic[name],position=0):

            #if name=="druid" and num=="4271":continue

            dic[name][num]["title"] = clean(dic[name][num]["title"])




            if dic[name][num]["body"]is not None:

                dic[name][num]["body"] = clean(dic[name][num]["body"])

            reviews=[]
            for review in dic[name][num]["reviews"]:

                reviews.append(clean(review))

            dic[name][num]["reviews"] =  " ".join(reviews)

            issue_comments=[]
            for issue_comment in dic[name][num]["issue_comments"]:

                issue_comments.append(clean(issue_comment))
            dic[name][num]["issue_comments"] = " ".join(issue_comments)

            review_comments=[]
            for review_comment in dic[name][num]["review_comments"]:

                review_comments.append(clean(review_comment))

            dic[name][num]["review_comments"] = " ".join(review_comments)
            '''
            commit_title=[]
            for title in dic[name][num]["commit_title"]:


                commit_title.append(clean(title))

            dic[name][num]["commit_title"] = " ".join(commit_title)

            commit_body=[]
            for body in dic[name][num]["commit_body"]:

                commit_body.append(clean(body))

            dic[name][num]["commit_body"] = " ".join(commit_body)
            '''
            for sha in dic[name][num].get("commit_comment",{}):
                commit_comments = []
                for comment in dic[name][num]["commit_comment"][sha]:


                    commit_comments.append(clean(comment))

                dic[name][num]["commit_comment"][sha] = " ".join(commit_comments)

        file = open('../data/pr_preprocess.dic', mode='w', encoding="utf-8")
        json.dump(dic, file, ensure_ascii=False, indent=2)
        file.close()

""""""""""""""""""

def processing_code():
    f = open('../data/code_comment_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    '''
    f.close()
    file = open("C:\\Users\\wty0511\\IdeaProjects\\Twitter-LDA-master\\data\\filelist_code_comment.txt", "w",
                encoding="utf-8")
    file.close()
    '''
    for name in dic:
        #file = open("C:\\Users\\wty0511\\IdeaProjects\\Twitter-LDA-master\\data\\Data4Model\\code_comment\\" + name + ".txt",
        #            "w", encoding="utf-8")
        for sha in tqdm(dic[name],position=0):

            multi_lines=[]
            for multi_line in dic[name][sha]["multi_line"]:
                multi_lines.append(clean(multi_line))

            #dic[name][sha]["multi_line"] =  ' '.join(multi_lines)
            dic[name][sha]["multi_line"] = multi_lines
            single_lines=[]
            for single_line in dic[name][sha]["single_line"]:
                single_lines.append(clean(single_line))
            #dic[name][sha]["single_line"] = ' '.join(single_lines)
            dic[name][sha]["single_line"] = single_lines
            #all=" ".join([dic[name][sha]["multi_line"], dic[name][sha]["single_line"]])
            #if not all.isspace():
                #file.write(all)
                #file.write('\n')
        file.close()
        #file= open("C:\\Users\\wty0511\\IdeaProjects\\Twitter-LDA-master\\data\\filelist_code_comment.txt","a",encoding="utf-8")
        #file.write(name+".txt")
        #file.write("\n")
        #file.close()


        file = open('../data/code_comment_clean_preprocessing.dic', mode='w', encoding="utf-8")
        json.dump(dic, file, ensure_ascii=False, indent=2)
        file.close()
""""""""""""""

def processing_commit():
    f = open('../data/commit_message_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()

    for name in dic:

        for sha in tqdm(dic[name]):
            try:
                dic[name][sha]["title"] = clean(dic[name][sha]["title"])
            except Exception as e:
                print("title")
                pass
            try:
                dic[name][sha]["body"] = clean(dic[name][sha]["body"])
            except Exception as e:
                pass

    file = open('./commit_message_preprocess.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()

def processing_pr_commit():
    f = open('commit_message_in_pr_cleaning.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()

    for name in dic:
        for num in tqdm(dic[name]):
            for sha in dic[name][num]:
                try:
                    dic[name][num][sha]["commit_title"] = clean(dic[name][num][sha]["commit_title"])
                except Exception as e:
                    pass
                try:

                    dic[name][num][sha]["commit_body"] = clean(dic[name][num][sha]["commit_body"])
                except Exception as e:
                    pass

    file = open('./commit_message_in_pr_preprocess.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()



def check(str):
    my_re = re.compile(r'[^A-Za-z]')

    res = re.findall(my_re, str)

    if len(res)>0:
        return False
    else:
        return True



if __name__ == '__main__':
    #processing_code()
    #processing_commit()
    #print(Counter(l).most_common(int(len(set(l))*0.01)))
    #print(check("리프레시로"))
    #processing_pr_commit()
    #processing_commit()
    processing_code()