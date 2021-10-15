import os
import json
import math
import urllib.request
import sys
import git
import numpy as np
import enchant
from random import randint, sample
from tqdm import tqdm
from git import Git
from git.repo import Repo
from git.repo.fun import is_git_dir
import  pandas as pd


import Algorithmia


import re
# 遍历文件夹

r20=re.compile(
    r'\d')
f=open('../data/emoj.txt','r',encoding='utf-8')
emoj=[x.strip('\n') for x in f.readlines()]
f.close()
f=open('../data/html.txt','r',encoding='utf-8')
html=[x.strip('\n') for x in f.readlines()]
f.close()
def walkFile(file):
    i=0
    dic={}
    l=[]
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            print(f)
            str = os.path.join(root, f)
            df = pd.read_csv(str)
            project_name=f.split('_')[0]

            print(i)
            dic[project_name]={}
            for tup in tqdm(df.itertuples()):
                i += 1
                dic[project_name][tup[2]]={}
                l.append(tup[2])
                dic[project_name][tup[2]]['title'] = tup[5]
                dic[project_name][tup[2]]['body'] = tup[6]
    #file = open('../data/commit_message.dic', mode='w', encoding="utf-8")
    #json.dump(dic, file, ensure_ascii=False, indent=2)
    #file.close()
    print(len(set(l)))
def main():
    walkFile("../data/genealogy")

def cleaning():
    f = open('../data/commit_message.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    #url
    url = re.compile(
        r"""(?:(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm|content|single|ha)://[^<>\s]+|(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm)://|(?:(?:(?:[^\s!@#$%^&*()_=+[\]{}\|;:'",.<>/?]+)\.)+(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)\b|(?:(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))(?:[;/][^#?<>\s]*)?(?:\?[^#<>\s]*)?(?:#[^<>\s]*)?)""")
    merge1 = re.compile(
        r"""Merge branch[\s]+[\S]*[\s]+into[\s]+[\S]*""")

    merge2 = re.compile(
        r"""Merge branch[\s]+[\S]*[\s]of[\s]+[\S]*[\s]+into[\s]+[\S]*""")
    merge3 = re.compile(
        r"""Merge branch[\s]+[\S]*""")
    merge4 = re.compile(
        r"""Merge remote[\s]*-[\s]*tracking[\s]+branch""")

    merge5 = re.compile(
        r"""Merge remote[\s]*-[\s]*tracking[\s]+branch[\s]+[\S]*[\s]+into[\s]+[\S]*""")

    #file
    file_path = re.compile(
        r"""(?:(?:[^/ ()\[\]]+/)*(?:[^/ ()\[\]])+(?:\.(?:tex|xml|git|cpp|less|x|html|scala|asciidoc|xls|db|testutils|importorder|gradle|prefab|k|tsx|out|txt|xlsx|conf|X|png|dust|jar|pdf|sh|js|groovy|json|java|properties|css|lua|yam|csv))\b)""")
    #code1
    code1 = re.compile(
        r"(?:```(?:[\s\S]*?)```)")
    code2 = re.compile(
        r"(?:`(?:[\s\S]*?)`)")
    #function
    function = re.compile(
    r"(?:[a-zA-Z_][a-zA-Z\d_]*)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1}(?:\.(?:[a-zA-Z_][a-zA-Z\d_]*)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1})+")

    #r"(?:[a-zA-Z\d_])+(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1}(?:\.(?:[a-zA-Z\d_]+)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\))*)*(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\))")
    #path
    path = re.compile(
        r"(?:[^\s/]+/)+(?:[^\s/]+)")
    # image
    image = re.compile(
        r"(!(\[([^\[\]]*?)\])\([^\[\]]*?\))")
    # issues
    issues = re.compile(
        r"#\d+")
    # TASK LISTS
    task_list = re.compile(
        r"(?:- \[x\]|- \[ \])")
    # url
    url2 = re.compile(
        r"((\[([^\[\]]*?)\])\([^\[\]]*?\))")
    # 超链接
    hyperlink = re.compile(
        r"<a href=[\s\S]+?>")
    comment = re.compile(
        r"<!--[\s\S]+?-->")
    #sha
    sha = re.compile(
        r"[a-zA-Z\d]{40}")
    html_tag = re.compile(r'|'.join(html))
    emjo = re.compile(r'|'.join(emoj))
    xml_tag = re.compile(
        r'<[^<>]*?/>')

    punctuation = re.compile(
        r"""[`~!@#$%^&*()\-_=\+\{\}\[\]|\\:;"'<>?/,\.\n\r\t]""")
    digit = re.compile(
        r"\d")
    #name_at=re.compile(r'((-By|-by):[\s\S]*?<[\s\S]*?@>)')
    name_at = re.compile(r'(?:-by|-By):[\s\S]*?<[\s\S]*?@>|<[\s\S]*?@>')
    author=re.compile(r'(?:Author:)[\s\S]*?<[\s\S]*?>')
    space = re.compile(
        r"[ ]+")
    svn = re.compile(r'git-svn-id:[ ]+([^\s]+)?')
    tag = re.compile('r(?:[a-zA-Z_][a-zA-Z\d_]*)<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>|<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>')
    package = r"(?:[a-zA-Z_][a-zA-Z\d_]*\.)+(?:[a-zA-Z\d_()]+)"
    at_sb = re.compile(r'@([a-zA-Z_\d-]+)')
    merge_from=re.compile(r"Merge pull request from[\s\S]+]")
    buchong = re.compile(r"<ndj::NDA\*>|cid:<card id>|link:<itemName>|streamId:<id>|io\.realm:realm-annotations:<your_realm_version>|linux-<arch>-fedora")
    count=0
    for name in dic:
        print(name)
        for commit_id in tqdm(dic[name]):

            if not type(dic[name][commit_id]['title']) == float:
                count+=1
                '''
                if len(svn.findall(dic[name][commit_id]['title']))>0:
                    print(svn.findall(dic[name][commit_id]['title']))
                '''

                dic[name][commit_id]['title'] = re.sub(code1, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(code2, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(file_path, '', dic[name][commit_id]['title'])
                #dic[name][commit_id]['title'] = re.sub(function, '', dic[name][commit_id]['title'])
                result1 = image.findall(dic[name][commit_id]['title'])
                for i in result1:
                    dic[name][commit_id]['title'] = dic[name][commit_id]['title'].replace(
                        i[0], i[2])

                result1 = url2.findall(dic[name][commit_id]['title'])
                for i in result1:

                    dic[name][commit_id]['title'] = dic[name][commit_id]['title'].replace(
                        i[0],
                        i[2])
                result1 = url2.findall(dic[name][commit_id]['title'])
                for i in result1:

                    dic[name][commit_id]['title'] = dic[name][commit_id]['title'].replace(
                        i[0],
                        i[2])
                dic[name][commit_id]['title'] = re.sub(issues, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(task_list, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(hyperlink, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(comment, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(html_tag, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(emjo, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(xml_tag, '', dic[name][commit_id]['title'])


                #dic[name][commit_id]['title'] = re.sub(path, '', dic[name][commit_id]['title'])

                dic[name][commit_id]['title'] = re.sub(merge1, 'Merge branch into', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(merge2, 'Merge branch of into', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(merge3, 'Merge branch', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(merge5, 'Merge remote-tracking branch into', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(merge4, 'Merge remote-tracking branch', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = dic[name][commit_id]['title'].replace('\n', " ").replace('\r', " ").replace('\t',
                                                                                                                 " ")

                dic[name][commit_id]['title'] = re.sub(url, '', dic[name][commit_id]['title'])



                for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][commit_id]['title']):

                    flag = 1
                    for word in i.split('/'):
                        if (word != '' and not d.check(word)) or len(r20.findall(word)) > 0 or len(word)==1:
                            flag = 0
                    if not flag:
                        #print(i)
                        dic[name][commit_id]['title'] = dic[name][commit_id][
                            'title'].replace(i, "")


                for i in re.compile(package).findall(dic[name][commit_id]['title']):
                    if len(re.compile(r"\([\s\S]*?\)").findall(i))==0:
                        dic[name][commit_id]['title'] = dic[name][commit_id][
                            'title'].replace(i, "")


                dic[name][commit_id]['title'] = re.sub(digit, '', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(name_at, "-by", dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(author, "Author", dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(svn, 'git-svn-id:', dic[name][commit_id]['title'])




                if "Merge pull request from This reverts commit"not in  dic[name][commit_id]['title']:
                    dic[name][commit_id]['title'] = re.sub(merge_from, 'Merge pull request from ', dic[name][commit_id]['title'])

                dic[name][commit_id]['title'] = re.sub(at_sb, '', dic[name][commit_id]['title'])
                if commit_id != "eeb3dbe":
                    dic[name][commit_id]['title'] = re.sub(buchong, '', dic[name][commit_id]['title'])
                    dic[name][commit_id]['title'] = re.sub(tag, '', dic[name][commit_id]['title'])
                    dic[name][commit_id]['title'] = re.sub(tag, '', dic[name][commit_id]['title'])


                dic[name][commit_id]['title'] = re.sub(punctuation, ' ', dic[name][commit_id]['title'])
                dic[name][commit_id]['title'] = re.sub(space, ' ', dic[name][commit_id]['title'])


                for_check.append(dic[name][commit_id]['title'])

            if not type(dic[name][commit_id]['body']) == float:
                '''
                if len(svn.findall(dic[name][commit_id]['body'])) > 0:
                    print(svn.findall(dic[name][commit_id]['body']))
                '''
                count+=1
                dic[name][commit_id]['body'] = re.sub(code1, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(code2, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(file_path, '', dic[name][commit_id]['body'])
                #dic[name][commit_id]['body'] = re.sub(function, '', dic[name][commit_id]['body'])
                result1 = image.findall(dic[name][commit_id]['body'])
                for i in result1:

                    dic[name][commit_id]['body'] = dic[name][commit_id]['body'].replace(
                        i[0], i[2])

                result1 = url2.findall(dic[name][commit_id]['body'])
                for i in result1:

                    dic[name][commit_id]['body'] = dic[name][commit_id]['body'].replace(
                        i[0],
                        i[2])
                result1 = url2.findall(dic[name][commit_id]['body'])
                for i in result1:

                    dic[name][commit_id]['body'] = dic[name][commit_id]['body'].replace(
                        i[0],
                        i[2])
                dic[name][commit_id]['body'] = re.sub(issues, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(task_list, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(url2, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(url2, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(hyperlink, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(comment, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(html_tag, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(emjo, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(sha, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(xml_tag, '', dic[name][commit_id]['body'])

                #dic[name][commit_id]['body'] = re.sub(path, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(merge1, 'Merge branch into', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(merge2, 'Merge branch of into', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(merge3, 'Merge branch', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(merge5, 'Merge remote-tracking branch into', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(merge4, 'Merge remote-tracking branch', dic[name][commit_id]['body'])

                dic[name][commit_id]['body'] = dic[name][commit_id]['body'].replace('\n', " ").replace('\r', " ").replace('\t',
                                                                                                                  " ")



                dic[name][commit_id]['body'] = re.sub(url, '', dic[name][commit_id]['body'])

                for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][commit_id]['body']):
                    flag = 1
                    for word in i.split('/'):
                        if (word != '' and not d.check(word)) or len(r20.findall(word)) > 0 or len(word)==1:
                            flag = 0

                    if not flag:
                        #print(i)
                        dic[name][commit_id]['body'] = dic[name][commit_id][
                            'body'].replace(i, "")

                for i in re.compile(package).findall(dic[name][commit_id]['body']):
                    if len(re.compile(r"\([\s\S]*?\)").findall(i))==0:
                        dic[name][commit_id]['body'] = dic[name][commit_id][
                            'body'].replace(i, "")



                dic[name][commit_id]['body'] = re.sub(digit, '', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(name_at, "-by", dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(author, "Author", dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(svn, 'git-svn-id:', dic[name][commit_id]['body'])
                if "Merge pull request from This reverts commit"not in  dic[name][commit_id]['body']:
                    dic[name][commit_id]['body'] = re.sub(merge_from, 'Merge pull request from ', dic[name][commit_id]['body'])

                dic[name][commit_id]['body'] = re.sub(at_sb, '', dic[name][commit_id]['body'])
                if commit_id != "eeb3dbe":
                    dic[name][commit_id]['body'] = re.sub(buchong, '', dic[name][commit_id]['body'])
                    dic[name][commit_id]['body'] = re.sub(tag, '', dic[name][commit_id]['body'])
                    dic[name][commit_id]['body'] = re.sub(tag, '', dic[name][commit_id]['body'])

                dic[name][commit_id]['body'] = re.sub(punctuation, ' ', dic[name][commit_id]['body'])
                dic[name][commit_id]['body'] = re.sub(space, ' ', dic[name][commit_id]['body'])

                for_check.append(dic[name][commit_id]['body'])



    #file = open('../data/commit_message_clean.dic', mode='w', encoding="utf-8")
    #json.dump(dic, file, ensure_ascii=False, indent=2)
    #file.close()
    print(count)

def cleaning_commit_pr():
    f = open('../data/commit_message_in_pr.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    # url
    url = re.compile(
        r"""(?:(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm|content|single|ha)://[^<>\s]+|(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm)://|(?:(?:(?:[^\s!@#$%^&*()_=+[\]{}\|;:'",.<>/?]+)\.)+(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)\b|(?:(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))(?:[;/][^#?<>\s]*)?(?:\?[^#<>\s]*)?(?:#[^<>\s]*)?)""")

    merge1 = re.compile(
        r"""Merge branch[\s]+[\S]*[\s]+into[\s]+[\S]*""")

    merge2 = re.compile(
        r"""Merge branch[\s]+[\S]*[\s]of[\s]+[\S]*[\s]+into[\s]+[\S]*""")
    merge3 = re.compile(
        r"""Merge branch[\s]+[\S]*""")
    merge4 = re.compile(
        r"""Merge remote[\s]*-[\s]*tracking[\s]+branch""")

    merge5 = re.compile(
        r"""Merge remote[\s]*-[\s]*tracking[\s]+branch[\s]+[\S]*[\s]+into[\s]+[\S]*""")

    # file
    file_path = re.compile(
        r"""(?:(?:[^/ ()\[\]]+/)*(?:[^/ ()\[\]])+(?:\.(?:tex|xml|git|cpp|less|x|html|scala|asciidoc|xls|db|testutils|importorder|gradle|prefab|k|tsx|out|txt|xlsx|conf|X|png|dust|jar|pdf|sh|js|groovy|json|java|properties|css|lua|yam|csv))\b)""")

    # code1
    code1 = re.compile(
        r"(?:```(?:[\s\S]*?)```)")
    code2 = re.compile(
        r"(?:`(?:[\s\S]*?)`)")
    # function
    function = re.compile(
        r"(?:[a-zA-Z_][a-zA-Z\d_]*)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1}(?:\.(?:[a-zA-Z_][a-zA-Z\d_]*)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1})+")

    # r"(?:[a-zA-Z\d_])+(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\)){0,1}(?:\.(?:[a-zA-Z\d_]+)(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\))*)*(?:\(\)|\(\.\.\)|\([a-zA-Z\d_]+(,[a-zA-Z\d_]+)*\))")
    # path
    path = re.compile(
        r"(?:[^\s/]+/)+(?:[^\s/]+)")
    # image
    image = re.compile(
        r"(!(\[([^\[\]]*?)\])\([^\[\]]*?\))")
    # issues
    issues = re.compile(
        r"#\d+")
    # TASK LISTS
    task_list = re.compile(
        r"(?:- \[x\]|- \[ \])")
    # url
    url2 = re.compile(
        r"((\[([^\[\]]*?)\])\([^\[\]]*?\))")
    # 超链接
    hyperlink = re.compile(
        r"<a href=[\s\S]+?>")
    comment = re.compile(
        r"<!--[\s\S]+?-->")
    # sha
    sha = re.compile(
        r"[a-zA-Z\d]{40}")
    html_tag = re.compile(r'|'.join(html))

    emjo = re.compile(r'|'.join(emoj))
    xml_tag = re.compile(
        r'<[^<>]*?/>')

    punctuation = re.compile(
        r"""[`~!@#$%^&*()\-_=\+\{\}\[\]|\\:;"'<>?/,\.\n\r\t]""")
    digit = re.compile(
        r"\d")
    tag = re.compile('r(?:[a-zA-Z_][a-zA-Z\d_]*)<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>|<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>')
    name_at = re.compile(r'(?:-by|-By):[\s\S]*?<[\s\S]*?@>|<[\s\S]*?@>')
    author=re.compile(r'(?:Author:)[\s\S]*?<[\s\S]*?>')
    space = re.compile(
        r"[ ]+")
    svn = re.compile(r'(?:git-svn-id:)(?:[\s\S]*?])')
    package = r"(?:[a-zA-Z_][a-zA-Z\d_]*\.)+(?:[a-zA-Z\d_()]+)"
    at_sb = re.compile(r'@([a-zA-Z_\d-]+)')
    merge_from = re.compile(r"Merge pull request from[\s\S]+]")
    buchong = re.compile(r"<ndj::NDA\*>|cid:<card id>|link:<itemName>|streamId:<id>|io\.realm:realm-annotations:<your_realm_version>|linux-<arch>-fedora")
    count=0
    for name in dic:
        print(name)
        for num in tqdm(dic[name]):
            for commit_id in dic[name][num]:
                if dic[name][num][commit_id]=={}:continue
                count+=1

                dic[name][num][commit_id]['commit_title'] = re.sub(code1, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(code2, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(file_path, '', dic[name][num][commit_id]['commit_title'])
                # dic[name][num][commit_id]['commit_title'] = re.sub(function, '', dic[name][num][commit_id]['commit_title'])
                result1 = image.findall(dic[name][num][commit_id]['commit_title'])
                for i in result1:

                    dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace(i[0], i[2])

                result1 = url2.findall(dic[name][num][commit_id]['commit_title'])
                for i in result1:

                    dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace(i[0],
                                                                                                                  i[2])
                result1 = url2.findall(dic[name][num][commit_id]['commit_title'])
                for i in result1:

                    dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace(i[0],
                                                                                                                  i[2])
                dic[name][num][commit_id]['commit_title'] = re.sub(issues, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(task_list, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(hyperlink, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(comment, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(html_tag, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(emjo, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(xml_tag, '', dic[name][num][commit_id]['commit_title'])

                # dic[name][num][commit_id]['commit_title'] = re.sub(path, '', dic[name][num][commit_id]['commit_title'])

                dic[name][num][commit_id]['commit_title'] = re.sub(merge1, 'Merge branch into', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(merge2, 'Merge branch of into', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(merge3, 'Merge branch', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(merge5, 'Merge remote-tracking branch into',
                                                       dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(merge4, 'Merge remote-tracking branch',
                                                       dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace('\n', " ").replace('\r',
                                                                                                         " ").replace(
                    '\t',
                    " ")
                dic[name][num][commit_id]['commit_title'] = re.sub(url, '', dic[name][num][commit_id]['commit_title'])

                for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num][commit_id]['commit_title']):

                    flag = 1
                    for word in i.split('/'):
                        if (word != '' and not d.check(word)) or len(r20.findall(word)) > 0 or len(word)==1:
                            flag = 0

                    if not flag:
                        #print(i)
                        dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace(i, "")

                for i in re.compile(package).findall(dic[name][num][commit_id]['commit_title']):
                    if  len(re.compile(r"\([\s\S]*?\)").findall(i))==0:
                        dic[name][num][commit_id]['commit_title'] = dic[name][num][commit_id]['commit_title'].replace(i, "")

                dic[name][num][commit_id]['commit_title'] = re.sub(digit, '', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(name_at, "-by",dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(author, "Author",dic[name][num][commit_id]['commit_title'])


                if "Merge pull request from This reverts commit"not in  dic[name][num][commit_id]['commit_title']:
                    dic[name][num][commit_id]['commit_title'] = re.sub(merge_from, 'Merge pull request from ', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(at_sb, "", dic[name][num][commit_id]['commit_title'])

                if commit_id != "eeb3dbe":
                    dic[name][num][commit_id]['commit_title'] = re.sub(buchong, "",
                                                                       dic[name][num][commit_id]['commit_title'])
                    dic[name][num][commit_id]['commit_title'] = re.sub(tag, "",dic[name][num][commit_id]['commit_title'])
                    dic[name][num][commit_id]['commit_title'] = re.sub(tag, "", dic[name][num][commit_id]['commit_title'])


                dic[name][num][commit_id]['commit_title'] = re.sub(punctuation, ' ', dic[name][num][commit_id]['commit_title'])
                dic[name][num][commit_id]['commit_title'] = re.sub(space, ' ', dic[name][num][commit_id]['commit_title'])

                for_check.append(dic[name][num][commit_id]['commit_title'])



                dic[name][num][commit_id]['commit_body'] = re.sub(code1, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(code2, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(file_path, '', dic[name][num][commit_id]['commit_body'])
                # dic[name][num][commit_id]['commit_body'] = re.sub(function, '', dic[name][num][commit_id]['commit_body'])
                result1 = image.findall(dic[name][num][commit_id]['commit_body'])
                for i in result1:

                    dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id]['commit_body'].replace(
                        i[0], i[2])

                result1 = url2.findall(dic[name][num][commit_id]['commit_body'])
                for i in result1:

                    dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id]['commit_body'].replace(
                        i[0],
                        i[2])
                result1 = url2.findall(dic[name][num][commit_id]['commit_body'])
                for i in result1:

                    dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id]['commit_body'].replace(
                        i[0],
                        i[2])
                dic[name][num][commit_id]['commit_body'] = re.sub(issues, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(task_list, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(hyperlink, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(comment, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(html_tag, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(emjo, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(sha, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(xml_tag, '', dic[name][num][commit_id]['commit_body'])

                # dic[name][num][commit_id]['commit_body'] = re.sub(path, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(merge1, 'Merge branch into', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(merge2, 'Merge branch of into', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(merge3, 'Merge branch', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(merge5, 'Merge remote-tracking branch into',
                                                      dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(merge4, 'Merge remote-tracking branch',
                                                      dic[name][num][commit_id]['commit_body'])

                dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id]['commit_body'].replace('\n', " ").replace('\r',
                                                                                                       " ").replace(
                    '\t',
                    " ")
                dic[name][num][commit_id]['commit_body'] = re.sub(url, '', dic[name][num][commit_id]['commit_body'])

                for i in re.compile(r"""(?:[^/ ()\[\]'"“‘:;,]+/)+(?:[^/ ()\[\]'"“‘:;,]+)[/]*""").findall(
                        dic[name][num][commit_id]['commit_body']):

                    flag = 1
                    for word in i.split('/'):
                        if (word != '' and not d.check(word)) or len(r20.findall(word)) > 0 or len(word)==1:

                            flag = 0
                    if not flag:
                        #print(i)
                        dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id]['commit_body'].replace(i, "")

                for i in re.compile(package).findall(dic[name][num][commit_id]['commit_body']):
                    if  len(re.compile(r"\([\s\S]*?\)").findall(i)) == 0:
                        dic[name][num][commit_id]['commit_body'] = dic[name][num][commit_id][
                            'commit_body'].replace(i, "")


                dic[name][num][commit_id]['commit_body'] = re.sub(digit, '', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(name_at, "-by",dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(author, "Author",dic[name][num][commit_id]['commit_body'])

                if "Merge pull request from This reverts commit" not in dic[name][num][commit_id]['commit_body']:
                    dic[name][num][commit_id]['commit_body'] = re.sub(merge_from, 'Merge pull request from ',
                                                                       dic[name][num][commit_id]['commit_title'])

                dic[name][num][commit_id]['commit_body'] = re.sub(at_sb, "", dic[name][num][commit_id]['commit_body'])


                if commit_id!="eeb3dbe":
                    dic[name][num][commit_id]['commit_body'] = re.sub(buchong, "",
                                                                      dic[name][num][commit_id]['commit_body'])
                    dic[name][num][commit_id]['commit_body'] = re.sub(tag, "", dic[name][num][commit_id]['commit_body'])
                    dic[name][num][commit_id]['commit_body'] = re.sub(tag, "", dic[name][num][commit_id]['commit_body'])

                dic[name][num][commit_id]['commit_body'] = re.sub(punctuation, ' ', dic[name][num][commit_id]['commit_body'])
                dic[name][num][commit_id]['commit_body'] = re.sub(space, ' ', dic[name][num][commit_id]['commit_body'])
                for_check.append(dic[name][num][commit_id]['commit_body'])

    #file = open('../data/commit_message_in_pr_cleaning.dic', mode='w', encoding="utf-8")
    #json.dump(dic, file, ensure_ascii=False, indent=2)
    #file.close()
    print(count)
def Sample():
    f = open('commit_message.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    l=[]
    for name in dic:
        for commit_id in dic[name]:
            try:
                if len(dic[name][commit_id]['title'])>0:
                    l.append(dic[name][commit_id]['title'])
            except:
                pass
            try:
                if len(dic[name][commit_id]['body']) > 0:
                    l.append(dic[name][commit_id]['body'])

            except:
                pass
    print(len(l))
    return set(l)

def test(pattern):
    f = open('commit_message.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    l=[]
    for name in dic:
        for commit_id in dic[name]:
            try:
                l.extend(pattern.findall(dic[name][commit_id]['title']))
            except:
                pass
            try:
                l.extend(pattern.findall(dic[name][commit_id]['body']))
            except:
                pass

    return l
if __name__ == '__main__':
    for_check=[]

    '''
    f = open('./commit_message.dic', mode='r', encoding="utf-8")
    dic = json.load(f)
    f.close()
    sta={}
    l=[]
    for name in dic:
        sta[name] = {
            'project_name':name,
            'title': 0,
            'body':0,
        }
        for commit_id in dic[name]:

            if not isinstance(dic[name][commit_id]['title'], float):
                sta[name]['title']+=1
            if not isinstance(dic[name][commit_id]['body'], float):
                sta[name]['body']+=1
        l.append(sta[name])
    print(l)
    pd.DataFrame(l).to_csv('commit_message_statistic.csv')
    '''
    #main()
    #l=test(re.compile(r'by:[\s\S]*?<[\s\S]*?>'))
    #print(l)

    d = enchant.Dict("en_US")

    main()
    cleaning()
    cleaning_commit_pr()


