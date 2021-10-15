import json
from tqdm import tqdm
import re
from collections import Counter
from random import randint, sample
from nltk.corpus import wordnet
import nltk
import enchant

def search(pattern1):
    f = open('../data/pr_message(NL).dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    l=[]
    all=0
    for name in dic:
        print(name)
        for num in dic[name]:
            #dic[name][num]['title'] = dic[name][num]['title'].replace('\n', " ").replace('\r', " ").replace('\t', " ")
            result1 = pattern1.findall(dic[name][num]['title'])
            length = len(result1)
            all+=length
            if length > 0:
                #print(result1)
                l.extend(result1)


            try:
                #dic[name][num]['body'] =  dic[name][num]['body'].replace('\n',  " ").replace('\r',  " ").replace('\t',  " ")
                result1 = pattern1.findall(dic[name][num]['body'])
                length = len(result1)
                all += length
                if length > 0:
                    #print(result1)
                    l.extend(result1)
            except Exception as e:
                print(e)
                pass
            for i in range(len(dic[name][num]["issue_comments"])):
                #dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                result1 = pattern1.findall(dic[name][num]["issue_comments"][i])
                length = len(result1)
                all += length
                if length > 0:
                    #print(result1)
                    l.extend(result1)

            for j in range(len(dic[name][num]["review_comments"])):
                #dic[name][num]["review_comments"][j] = dic[name][num]["review_comments"][j].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                result1 = pattern1.findall(dic[name][num]["review_comments"][j])
                length = len(result1)
                all += length
                if length > 0:
                    #print(result1)
                    l.extend(result1)

            for k in range(len(dic[name][num]["reviews"])):
                #dic[name][num]["reviews"][k] = dic[name][num]["reviews"][k].replace('\n', " ").replace('\r',
                #                                                                                       " ").replace(
                #    '\t', " ")
                result1 = pattern1.findall(dic[name][num]["reviews"][k])
                length = len(result1)
                all += length
                if length > 0:
                    #print(result1)
                    l.extend(result1)
            try:
                for sha in dic[name][num]["commit_comment"]:
                    for i in range(len(dic[name][num]["commit_comment"][sha])):
                        result1 = pattern1.findall(dic[name][num]["commit_comment"][sha][k])
                        length = len(result1)
                        all += length
                        if length > 0:
                            # print(result1)
                            l.extend(result1)
            except:
                pass
    print(len(l))
    return l

def clean (pattern,to=''):
    f = open('../data/pr_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    for name in dic.keys():

        for num in dic[name].keys():
            #dic[name][num]['title'] = dic[name][num]['title'].replace('\n', " ").replace('\r', " ").replace('\t', " ")
            dic[name][num]['title'] = re.sub(pattern, to, dic[name][num]['title'])

            try:
                #dic[name][num]['body'] = dic[name][num]['body'].replace('\n', " ").replace('\r', " ").replace('\t', " ")
                dic[name][num]['body'] = re.sub(pattern, to, dic[name][num]['body'])

            except:
                pass
            for i in range(len(dic[name][num]["issue_comments"])):
                #dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                dic[name][num]["issue_comments"][i] = re.sub(pattern, to, dic[name][num]["issue_comments"][i])

            for i in range(len(dic[name][num]["review_comments"])):
                #dic[name][num]["review_comments"][i] = dic[name][num]["review_comments"][i].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                dic[name][num]["review_comments"][i] = re.sub(pattern, to, dic[name][num]["review_comments"][i])

            for i in range(len(dic[name][num]["reviews"])):
                #dic[name][num]["reviews"][i] = dic[name][num]["reviews"][i].replace('\n', " ").replace('\r',
                #                                                                                       " ").replace(
                #    '\t', " ")
                dic[name][num]["reviews"][i] = re.sub(pattern, to, dic[name][num]["reviews"][i])
                #
            try:
                for sha in dic[name][num]["commit_comment"]:
                    for i in range(len(dic[name][num]["commit_comment"][sha])):
                        dic[name][num]["commit_comment"][sha][i] = re.sub(pattern, to, dic[name][num]["commit_comment"][sha][i])
            except:
                pass
    file = open('../data/pr_clean.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()
def clean_s():
    f = open('../data/pr_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    for name in dic.keys():

        for num in dic[name].keys():
            dic[name][num]['title'] = dic[name][num]['title'].replace('\n', " ").replace('\r', " ").replace('\t', " ")

            try:
                dic[name][num]['body'] = dic[name][num]['body'].replace('\n', " ").replace('\r', " ").replace('\t', " ")

            except:
                pass
            for i in range(len(dic[name][num]["issue_comments"])):
                dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace('\n', " ").replace(
                    '\r', " ").replace('\t', " ")

            for i in range(len(dic[name][num]["review_comments"])):
                dic[name][num]["review_comments"][i] = dic[name][num]["review_comments"][i].replace('\n', " ").replace(
                    '\r', " ").replace('\t', " ")

            for i in range(len(dic[name][num]["reviews"])):
                dic[name][num]["reviews"][i] = dic[name][num]["reviews"][i].replace('\n', " ").replace('\r',
                                                                                                       " ").replace(
                    '\t', " ")
            try:
                for sha in dic[name][num]["commit_comment"]:
                    for j in range(len(dic[name][num]["commit_comment"][sha])):
                        dic[name][num]["commit_comment"][sha][j]=dic[name][num]["commit_comment"][sha][j].replace('\n', " ").replace('\r',
                                                                                                           " ").replace(
                        '\t', " ")
            except:
                pass
    file = open('../data/pr_clean.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()
def replace (pattern):
    f = open('../data/pr_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    for name in dic:
        print(name)
        for num in dic[name]:
            #dic[name][num]['title'] = dic[name][num]['title'].replace('\n', " ").replace('\r', " ").replace('\t', " ")
            result1 = pattern.findall(dic[name][num]['title'])
            for i in result1:
                dic[name][num]['title'] = dic[name][num]['title'].replace(i[0],i[2])



            try:
                #dic[name][num]['body'] =  dic[name][num]['body'].replace('\n',  " ").replace('\r',  " ").replace('\t',  " ")

                result1 = pattern.findall(dic[name][num]["body"])
                for j in result1:
                    dic[name][num]['body'] = dic[name][num]['body'].replace(j[0],j[2])

            except Exception as e:
                pass
            for i in range(len(dic[name][num]["issue_comments"])):
                #dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                result1 = pattern.findall(dic[name][num]["issue_comments"][i])
                for j in result1:
                    dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace(j[0],j[2])

            for i in range(len(dic[name][num]["review_comments"])):
                #dic[name][num]["review_comments"][j] = dic[name][num]["review_comments"][j].replace('\n', " ").replace(
                #    '\r', " ").replace('\t', " ")
                result1 = pattern.findall(dic[name][num]["review_comments"][i])
                for j in result1:
                    dic[name][num]["review_comments"][i] = dic[name][num]["review_comments"][i].replace(j[0], j[2])

            for i in range(len(dic[name][num]["reviews"])):
                #dic[name][num]["reviews"][k] = dic[name][num]["reviews"][k].replace('\n', " ").replace('\r',
                #                                                                                       " ").replace(
                #    '\t', " ")
                result1 = pattern.findall(dic[name][num]["reviews"][i])
                for j in result1:
                    dic[name][num]["reviews"][i] = dic[name][num]["reviews"][i].replace(j[0], j[2])
            try:
                for sha in dic[name][num]["commit_comment"]:
                    for i in range(len(dic[name][num]["commit_comment"][sha])):
                        result1 = pattern.findall(dic[name][num]["commit_comment"][sha][i])
                        for j in result1:
                            dic[name][num]["commit_comment"][sha][i] = dic[name][num]["commit_comment"][sha][i].replace(j[0], j[2])
            except Exception as e:
                pass
    file = open('../data/pr_clean.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()





def remake():
    f = open('../data/pr_message(NL).dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()

    file = open('../data/pr_clean.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()
def process():
    #多行代码
    clean(code1)
    # 单行代码
    clean(code2)


    clean(at_sb)
    # sha
    clean(sha)
    # image
    replace(image)
    # issues
    clean(task_list)
    # TASK LISTS
    clean(issues)
    # url
    replace(url2)
    replace(url2)

    # 超链接
    clean(hyperlink)
    #htmltag
    clean(re.compile(r'|'.join(html)))
    #xml
    clean(xml_tag)
    #注释
    clean(comment)
    clean(tag)
    #file
    clean(file_path)
    #emoj
    clean(r'|'.join(emoj))
    #\n\t\r
    clean_s()
    # url
    clean(url)
    package_file()


    clean(punctuation," ")
    clean(digit)
    clean(space," ")
def package_file():
    f = open('../data/pr_clean.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()

    for name in dic.keys():

        for num in dic[name].keys():


            for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                    dic[name][num]['title']):

                flag = 1
                for word in i.split('/'):
                    if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                        flag = 0
                if not flag:

                    print(i)
                    # print(i)
                    dic[name][num]['title'] = dic[name][num][
                        'title'].replace(i, "")

            for i in re.compile(package).findall(dic[name][num]['title']):
                if len(re.compile(r"\([\s\S]*?\)").findall(i)) == 0:
                    dic[name][num]['title'] = dic[name][num][
                        'title'].replace(i, "")


            try:
                for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num]['body']):

                    flag = 1
                    for word in i.split('/'):
                        if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                            print(i)
                    if not flag:
                        # print(i)
                        dic[name][num]['body'] = dic[name][num][
                            'body'].replace(i, "")

                for i in re.compile(package).findall(dic[name][num]['body']):
                    if len(re.compile(r"\([\s\S]*?\)").findall(i)) == 0:
                        dic[name][num]['body'] = dic[name][num][
                            'body'].replace(i, "")

            except:
                pass
            for i in range(len(dic[name][num]["issue_comments"])):
                for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num]["issue_comments"][i]):

                    flag = 1
                    for word in j.split('/'):
                        if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                            flag = 0
                            if len(word) == 1:
                                print(j)
                    if not flag:
                        # print(i)
                        dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace(j, "")

                for j in re.compile(package).findall(dic[name][num]['issue_comments'][i]):
                    if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                        dic[name][num]["issue_comments"][i] = dic[name][num]["issue_comments"][i].replace(j, "")

            for i in range(len(dic[name][num]["review_comments"])):
                for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num]["review_comments"][i]):

                    flag = 1
                    for word in j.split('/'):
                        if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                            flag = 0
                            print(j)
                    if not flag:
                        # print(i)
                        dic[name][num]["review_comments"][i] = dic[name][num]["review_comments"][i].replace(j, "")

                for j in re.compile(package).findall(dic[name][num]['review_comments'][i]):
                    if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                        dic[name][num]["review_comments"][i] = dic[name][num]["review_comments"][i].replace(j, "")

            for i in range(len(dic[name][num]["reviews"])):
                for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num]["reviews"][i]):
                    flag = 1
                    for word in j.split('/'):
                        if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                            flag = 0
                            print(j)
                    if not flag:

                        dic[name][num]["reviews"][i] = dic[name][num]["reviews"][i].replace(j, "")

                for j in re.compile(package).findall(dic[name][num]['reviews'][i]):
                    if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                        dic[name][num]["reviews"][i] = dic[name][num]["reviews"][i].replace(j, "")
            try:
                for sha in dic[name][num]["commit_comment"]:
                    for i in range(len(dic[name][num]["commit_comment"][sha])):
                        for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                                dic[name][num]["commit_comment"][sha][i]):

                            flag = 1
                            for word in j.split('/'):
                                if (word != '' and not d.check(word)) or len(digit.findall(word)) > 0 or len(word) == 1:
                                    flag = 0
                                    print(j)
                            if not flag:
                                # print(i)
                                dic[name][num]["commit_comment"][sha][i] = dic[name][num]["commit_comment"][sha][i].replace(j, "")

                        for j in re.compile(package).findall(dic[name][num]["commit_comment"][sha][i]):
                            if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                                dic[name][num]["commit_comment"][sha][i] = dic[name][num]["commit_comment"][sha][i].replace(j, "")


            except:
                pass

    file = open('../data/pr_clean.dic', mode='w', encoding="utf-8")
    json.dump(dic, file, ensure_ascii=False, indent=2)
    file.close()





f=open('../data/emoj.txt','r',encoding='utf-8')
emoj=[x.strip('\n') for x in f.readlines()]
print(r'|'.join(emoj))
f.close()
f=open('../data/html.txt','r',encoding='utf-8')
html=[x.strip('\n') for x in f.readlines()]
f.close()


#url
url = re.compile(
    r"""(?:(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm|content|single|ha)://[^<>\s]+|(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm)://|(?:(?:(?:[^\s!@#$%^&*()_=+[\]{}\|;:'",.<>/?]+)\.)+(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)\b|(?:(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))(?:[;/][^#?<>\s]*)?(?:\?[^#<>\s]*)?(?:#[^<>\s]*)?)""")
# file
file_path = re.compile(
    r"""(?:(?:[^/ ()\[\]]+/)*(?:[^/ ()\[\]])+(?:\.(?:tex|xml|git|cpp|less|x|html|scala|asciidoc|xls|db|testutils|importorder|gradle|prefab|k|tsx|out|txt|xlsx|conf|X|png|dust|jar|pdf|sh|js|groovy|json|java|properties|css|lua|yam|csv))\b)""")
# code1
code1 = re.compile(
    r"(?:```(?:[\s\S]*?)```)")
code2 = re.compile(
    r"(?:`(?:[\s\S]*?)`)")

#sha
sha = re.compile(
                r"[a-zA-Z\d]{40}")

#image
image = re.compile(
    r"(!(\[([^\[\]]*?)\])\([^\[\]]*?\))")
#issues
issues = re.compile(
    r"#\d+")
#TASK LISTS
task_list = re.compile(
    r"(?:- \[x\]|- \[ \])")
#url
url2 = re.compile(
    r"((\[([^\[\]]*?)\])\([^\[\]]*?\))")


#超链接
hyperlink=re.compile(
    r"<a href=[\s\S]+?>")
comment=re.compile(
    r"<!--[\s\S]+?-->")
xml_tag=re.compile(
    r'<[^<>]*?/>')
at_sb=re.compile(
    r'@[a-zA-Z\d-]+')

punctuation = re.compile(
    r"""[`~!@#$%^&*()\-_=\+\{\}\[\]|\\:;"'<>?/,\.\n\r\t]""")
digit = re.compile(
    r"\d")
tag = re.compile('r(?:[a-zA-Z_][a-zA-Z\d_]*)<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>|<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>')
space=re.compile(
    r"[ ]+"
)
package = r"(?:[a-zA-Z_][a-zA-Z\d_]*\.)+(?:[a-zA-Z\d_()]+)"


d = enchant.Dict("en_US")
remake()
process()


