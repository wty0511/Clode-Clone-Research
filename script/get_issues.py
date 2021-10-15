import time

from github import Github
import json
from tqdm import tqdm


#和get_commit_message_pr.py一起使用补充查不到的部分

g = Github(login_or_token="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")

file = open('./not_found.txt', mode='r', encoding="utf-8")
l=file.readlines()
file.close()
f = open('../data/commit_message_in_pr.dic', mode='r', encoding="utf-8")
res = json.load(f)
f.close()
sum=0
for line in tqdm(l):
    sum+=1
    line=line.strip('\n')
    project_name,num,sha=line.split('^')
    try:
        c=g.search_issues(sha)
        time.sleep(2)
        for i in c:
            if i.number!=int(num):continue
            res[project_name][num][sha]['commit_title'] = i.title
            res[project_name][num][sha]['commit_body'] = i.body
        if sum%100==0:
            file = open('./commit_message_in_pr.dic', mode='w', encoding="utf-8")
            json.dump(res,file,ensure_ascii=False,indent=2)
            file.close()
    except Exception as e:
        print(e)
        f = open("error.txt", 'a')
        f.write(project_name)
        f.write('^')
        f.write(num)
        f.write('^')
        f.write(sha)
        f.write('\n')
        f.close()

file = open('../data/commit_message_in_pr.dic', mode='w', encoding="utf-8")
json.dump(res,file,ensure_ascii=False,indent=2)
file.close()


